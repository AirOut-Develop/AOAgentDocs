"""Validate an installed AOAgentDocs project without modifying it."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit


ALLOWED_PLATFORMS = {"server", "ios", "android", "web"}
ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
STATUS_BY_KIND = {
    "prd": {"draft", "in_review", "approved", "superseded", "withdrawn"},
    "design": {"draft", "in_review", "approved", "superseded", "withdrawn"},
    "adr": {"draft", "in_review", "approved", "superseded", "withdrawn"},
    "plan": {"planned", "in_progress", "blocked", "done", "cancelled"},
    "work": {"planned", "in_progress", "blocked", "done", "cancelled"},
    "issue": {"planned", "in_progress", "blocked", "done", "cancelled"},
    "verification": {"not_run", "passed", "failed", "waived"},
    "release": {"not_deployed", "canary", "released", "rolled_back"},
}
ID_ARRAY_FIELDS = ("refs", "evidence", "requirements", "covers")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]*)\)")
REFERENCE_DEFINITION_PATTERN = re.compile(
    r"^[ \t]{0,3}\[([^\]]+)\]:[ \t]*(<[^>]*>|\S+)(?:[ \t]+.*)?$", re.MULTILINE
)
REFERENCE_USE_PATTERN = re.compile(r"!?\[([^\]]+)\]\[([^\]]*)\]")
FENCE_PATTERN = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
INLINE_CODE_PATTERN = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", re.DOTALL)


def _load_json(path: Path, label: str, errors: list[str]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError:
        errors.append(f"{label}: file is missing")
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON at line {exc.lineno}, column {exc.colno}")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: cannot be read: {exc}")
    return None


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _safe_relative(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    path = PurePosixPath(value)
    return (
        value == path.as_posix()
        and not path.is_absolute()
        and ".." not in path.parts
        and "." not in path.parts
    )


def _has_symlink(path: Path, root: Path) -> bool:
    if root.is_symlink():
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _contained(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except (OSError, ValueError):
        return False


def _validate_platform_array(
    value: Any, label: str, errors: list[str], allowed: set[str] = ALLOWED_PLATFORMS
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label}: must be an array")
        return []
    valid: list[str] = []
    seen: set[str] = set()
    for platform in value:
        if not isinstance(platform, str) or platform not in allowed:
            errors.append(f"{label}: invalid platform {platform!r}")
        elif platform in seen:
            errors.append(f"{label}: duplicate platform {platform!r}")
        else:
            valid.append(platform)
            seen.add(platform)
    return valid


def _validate_project(data: Any, errors: list[str]) -> tuple[set[str], set[str]]:
    label = ".aodocs/project.json"
    if not isinstance(data, dict):
        errors.append(f"{label}: top level must be an object")
        return set(), set()
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append(f"{label}: schema_version must be 1")
    if not _is_nonempty_string(data.get("project_id")):
        errors.append(f"{label}: project_id must be a nonempty string")
    platforms = _validate_platform_array(data.get("platforms"), f"{label} platforms", errors)
    planned = _validate_platform_array(
        data.get("planned_platforms"), f"{label} planned_platforms", errors
    )
    overlap = set(platforms) & set(planned)
    if overlap:
        errors.append(
            f"{label}: platforms cannot be both active and planned: {', '.join(sorted(overlap))}"
        )
    return set(platforms + planned), set(planned) - set(platforms)


def _validate_id_array(record: dict[str, Any], field: str, label: str, errors: list[str]) -> list[str]:
    if field not in record:
        return []
    value = record[field]
    if not isinstance(value, list):
        errors.append(f"{label}.{field}: must be an array of IDs")
        return []
    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not ID_PATTERN.fullmatch(item):
            errors.append(f"{label}.{field}: invalid ID {item!r}")
        elif item in seen:
            errors.append(f"{label}.{field}: duplicate ID {item!r}")
        else:
            seen.add(item)
            result.append(item)
    return result


def _validate_document_path(
    target: Path, value: Any, label: str, errors: list[str]
) -> Path | None:
    if not _safe_relative(value):
        errors.append(f"{label}.path: must be a safe project-relative path")
        return None
    if PurePosixPath(value).suffix.lower() != ".md":
        errors.append(f"{label}.path: must name a Markdown (.md) file")
        return None
    path = target.joinpath(*PurePosixPath(value).parts)
    if not _contained(path, target):
        errors.append(f"{label}.path: escapes the project")
        return None
    if _has_symlink(path, target):
        errors.append(f"{label}.path: symlinks are not allowed")
        return None
    if not path.is_file():
        errors.append(f"{label}.path: Markdown file does not exist: {value}")
        return None
    return path


def _validate_records(
    data: Any,
    target: Path,
    project_platforms: set[str],
    planned_only_platforms: set[str],
    errors: list[str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[Path]]:
    manifest_label = ".aodocs/documents.json"
    if not isinstance(data, dict):
        errors.append(f"{manifest_label}: top level must be an object")
        return [], {}, []
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append(f"{manifest_label}: schema_version must be 1")
    documents = data.get("documents")
    if not isinstance(documents, list):
        errors.append(f"{manifest_label}: documents must be an array")
        return [], {}, []

    records: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    paths: list[Path] = []
    for index, item in enumerate(documents):
        label = f"{manifest_label} documents[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: must be an object")
            continue
        records.append(item)
        doc_id = item.get("id")
        if not isinstance(doc_id, str) or not ID_PATTERN.fullmatch(doc_id):
            errors.append(f"{label}.id: must be an uppercase alphanumeric/hyphen ID")
        elif doc_id in by_id:
            errors.append(f"{label}.id: duplicate document ID {doc_id!r}")
        else:
            by_id[doc_id] = item

        kind = item.get("kind")
        if not isinstance(kind, str) or kind not in STATUS_BY_KIND:
            errors.append(f"{label}.kind: invalid document kind {kind!r}")
        status = item.get("status")
        if not isinstance(status, str):
            errors.append(f"{label}.status: must be a string")
        elif isinstance(kind, str) and kind in STATUS_BY_KIND and status not in STATUS_BY_KIND[kind]:
            errors.append(f"{label}.status: {status!r} is invalid for kind {kind!r}")
        path = _validate_document_path(target, item.get("path"), label, errors)
        if path is not None:
            paths.append(path)
        revision = item.get("revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision <= 0:
            errors.append(f"{label}.revision: must be a positive integer")
        if not _is_nonempty_string(item.get("owner")):
            errors.append(f"{label}.owner: must be a nonempty string")
        record_platforms = _validate_platform_array(
            item.get("platforms"), f"{label}.platforms", errors, project_platforms
        )
        for field in ID_ARRAY_FIELDS:
            _validate_id_array(item, field, label, errors)

        if status == "approved":
            approval = item.get("approval")
            if not isinstance(approval, dict):
                errors.append(f"{label}.approval: approved documents require an object")
            else:
                for field in ("by", "at"):
                    if not _is_nonempty_string(approval.get(field)):
                        errors.append(f"{label}.approval.{field}: must be a nonempty string")
                approval_revision = approval.get("revision")
                if (
                    type(approval_revision) is not int
                    or approval_revision != revision
                ):
                    errors.append(f"{label}.approval.revision: must match document revision")
        if kind == "verification" and status == "passed":
            for field in ("command", "environment", "source_revision"):
                if not _is_nonempty_string(item.get(field)):
                    errors.append(f"{label}.{field}: passed verification requires a nonempty string")
        if kind == "verification" and status == "waived":
            for field in ("reason", "owner", "expires_at"):
                if not _is_nonempty_string(item.get(field)):
                    errors.append(f"{label}.{field}: waived verification requires a nonempty string")
        terminal_on_planned = kind == "verification" and status == "passed"
        terminal_on_planned = terminal_on_planned or (
            kind in {"plan", "work", "issue"} and status == "done"
            if isinstance(kind, str)
            else False
        )
        terminal_on_planned = terminal_on_planned or (
            kind == "release" and status == "released"
        )
        invalid_planned = sorted(set(record_platforms) & planned_only_platforms)
        if terminal_on_planned and invalid_planned:
            errors.append(
                f"{label} ({doc_id}): terminal status is not allowed on planned-only platforms: "
                f"{', '.join(invalid_planned)}"
            )
    return records, by_id, paths


def _validate_relationships(
    records: list[dict[str, Any]], by_id: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    requirement_owner: dict[str, str] = {}
    document_ids = set(by_id)
    for record in records:
        doc_id = record.get("id", "<invalid>")
        requirements = record.get("requirements", [])
        if isinstance(requirements, list):
            if requirements and record.get("kind") != "prd":
                errors.append(f"{doc_id}.requirements: requirements may only be declared by prd documents")
            if record.get("kind") == "prd":
                for requirement in requirements:
                    if not isinstance(requirement, str) or not ID_PATTERN.fullmatch(requirement):
                        continue
                    if requirement in requirement_owner:
                        errors.append(f"{doc_id}.requirements: duplicate requirement ID {requirement!r}")
                    elif requirement in document_ids:
                        errors.append(
                            f"{doc_id}.requirements: requirement ID {requirement!r} duplicates a document ID"
                        )
                    else:
                        requirement_owner[requirement] = str(doc_id)

    declared = set(requirement_owner)
    for record in records:
        doc_id = record.get("id", "<invalid>")
        for ref in record.get("refs", []) if isinstance(record.get("refs", []), list) else []:
            if isinstance(ref, str) and ID_PATTERN.fullmatch(ref) and ref not in by_id:
                errors.append(f"{doc_id}.refs: unknown document ID {ref!r}")
        evidence_ids = (
            record.get("evidence", []) if isinstance(record.get("evidence", []), list) else []
        )
        passed_evidence: list[dict[str, Any]] = []
        for evidence_id in evidence_ids:
            if not isinstance(evidence_id, str) or not ID_PATTERN.fullmatch(evidence_id):
                continue
            evidence = by_id.get(evidence_id)
            if evidence is None:
                errors.append(f"{doc_id}.evidence: unknown document ID {evidence_id!r}")
            elif evidence.get("kind") != "verification":
                errors.append(f"{doc_id}.evidence: {evidence_id!r} is not a verification document")
            elif evidence.get("status") == "passed":
                passed_evidence.append(evidence)
        covers = record.get("covers", []) if isinstance(record.get("covers", []), list) else []
        for requirement in covers:
            if isinstance(requirement, str) and ID_PATTERN.fullmatch(requirement) and requirement not in declared:
                errors.append(f"{doc_id}.covers: unknown requirement ID {requirement!r}")

        kind = record.get("kind")
        completed = (
            isinstance(kind, str)
            and kind in {"plan", "work", "issue"}
            and record.get("status") == "done"
        )
        completed = completed or (
            record.get("kind") == "release" and record.get("status") == "released"
        )
        if completed:
            if not passed_evidence:
                errors.append(f"{doc_id}: completed/released document requires at least one passed verification")
            evidence_covers: set[str] = set()
            for evidence in passed_evidence:
                value = evidence.get("covers", [])
                if isinstance(value, list):
                    evidence_covers.update(item for item in value if isinstance(item, str))
            for requirement in covers:
                if isinstance(requirement, str) and requirement in declared and requirement not in evidence_covers:
                    errors.append(
                        f"{doc_id}: requirement {requirement!r} is not covered by passed verification evidence"
                    )


def _validate_manifest(target: Path, data: Any, errors: list[str]) -> None:
    label = ".aodocs/manifest.json"
    if not isinstance(data, dict):
        errors.append(f"{label}: top level must be an object")
        return
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append(f"{label}: schema_version must be 1")
    kit_version = data.get("kit_version")
    if not _is_nonempty_string(kit_version):
        errors.append(f"{label}: kit_version must be a nonempty string")
    files = data.get("files")
    if not isinstance(files, dict):
        errors.append(f"{label}: files must be a path-to-sha256 object")
        return
    kit_root = target / ".aodocs" / "kit"
    kit_root_is_symlink = kit_root.is_symlink()
    if kit_root_is_symlink:
        errors.append(f"{label}: .aodocs/kit must not be a symlink")
    if "VERSION" not in files:
        errors.append(f"{label}: files must include VERSION")
    if "kit-files.json" not in files:
        errors.append(f"{label}: files must include managed kit-files.json")
    version_path = kit_root / "VERSION"
    version_is_symlink = kit_root_is_symlink or version_path.is_symlink()
    if version_is_symlink:
        errors.append(f"{label}: .aodocs/kit/VERSION must not be a symlink")
    else:
        try:
            installed_version = version_path.read_text(encoding="utf-8").strip()
            if installed_version != kit_version:
                errors.append(f"{label}: kit_version does not match .aodocs/kit/VERSION")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{label}: cannot read .aodocs/kit/VERSION: {exc}")

    trusted_index = False
    for relative, expected in files.items():
        if not _safe_relative(relative):
            errors.append(f"{label}: unsafe managed payload path {relative!r}")
            continue
        if not isinstance(expected, str) or not SHA256_PATTERN.fullmatch(expected):
            errors.append(f"{label}: invalid sha256 for {relative!r}")
            continue
        path = kit_root.joinpath(*PurePosixPath(relative).parts)
        if not _contained(path, kit_root) or _has_symlink(path, kit_root):
            errors.append(f"{label}: managed payload path is unsafe or a symlink: {relative!r}")
            continue
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(f"{label}: cannot read managed payload {relative!r}: {exc}")
            continue
        if actual != expected:
            errors.append(f"{label}: sha256 mismatch for managed payload {relative!r}")
        elif relative == "kit-files.json":
            trusted_index = True

    if not trusted_index:
        return
    index_label = ".aodocs/kit/kit-files.json"
    index = _load_json(kit_root / "kit-files.json", index_label, errors)
    if not isinstance(index, dict):
        if index is not None:
            errors.append(f"{index_label}: top level must be an object")
        return
    if type(index.get("schema_version")) is not int or index.get("schema_version") != 1:
        errors.append(f"{index_label}: schema_version must be 1")
    listed = index.get("files")
    if not isinstance(listed, list):
        errors.append(f"{index_label}: files must be an array")
        return
    valid_paths: list[str] = []
    seen: set[str] = set()
    for relative in listed:
        if not _safe_relative(relative):
            errors.append(f"{index_label}: unsafe payload path {relative!r}")
        elif relative in seen:
            errors.append(f"{index_label}: duplicate payload path {relative!r}")
        else:
            seen.add(relative)
            valid_paths.append(relative)
    if set(valid_paths) != set(files) or len(valid_paths) != len(files):
        errors.append(f"{label}: managed file keys must exactly match {index_label} files")


def _link_destination(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    # Markdown permits a title after an unbracketed destination.
    return value.split(maxsplit=1)[0]


def _without_fenced_code(text: str) -> str:
    kept: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = FENCE_PATTERN.match(line)
        if fence_character is None:
            if match:
                marker = match.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
            else:
                kept.append(line)
        elif match:
            marker = match.group(1)
            if marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
    return "".join(kept)


def _reference_label(value: str) -> str:
    return " ".join(value.split()).casefold()


def _validate_link_destination(
    target: Path, document: Path, destination: str, errors: list[str]
) -> None:
    if not destination:
        errors.append(f"{document.relative_to(target)}: empty relative link destination")
        return
    if destination.startswith("#") or "{" in destination or "}" in destination:
        return
    try:
        parsed = urlsplit(destination)
    except ValueError as exc:
        errors.append(f"{document.relative_to(target)}: malformed link {destination!r}: {exc}")
        return
    if parsed.scheme or parsed.netloc:
        return
    relative = unquote(parsed.path)
    if not relative:
        return
    linked = document.parent / relative
    if not _contained(linked, target) or _has_symlink(linked, target) or not linked.exists():
        errors.append(
            f"{document.relative_to(target)}: missing or unsafe relative link {destination!r}"
        )


def _validate_links(target: Path, documents: list[Path], errors: list[str]) -> None:
    for document in documents:
        try:
            text = document.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{document.relative_to(target)}: cannot inspect Markdown links: {exc}")
            continue
        text = INLINE_CODE_PATTERN.sub("", _without_fenced_code(text))
        definitions: set[str] = set()
        for match in REFERENCE_DEFINITION_PATTERN.finditer(text):
            definitions.add(_reference_label(match.group(1)))
            _validate_link_destination(
                target, document, _link_destination(match.group(2)), errors
            )
        for match in REFERENCE_USE_PATTERN.finditer(text):
            raw_label = match.group(2) or match.group(1)
            label = _reference_label(raw_label)
            if label not in definitions:
                errors.append(
                    f"{document.relative_to(target)}: undefined Markdown reference {raw_label!r}"
                )
        for match in LINK_PATTERN.finditer(text):
            destination = _link_destination(match.group(1))
            _validate_link_destination(target, document, destination, errors)


def _metadata_preflight(target: Path, errors: list[str]) -> bool:
    aodocs = target / ".aodocs"
    if _has_symlink(aodocs, target):
        errors.append(".aodocs: path components and metadata must not be symlinks")
        return False
    if aodocs.exists() and not aodocs.is_dir():
        errors.append(".aodocs: must be a directory")
        return False
    safe = True
    for name in ("project.json", "documents.json", "manifest.json"):
        path = aodocs / name
        if path.is_symlink():
            errors.append(f".aodocs/{name}: metadata must not be a symlink")
            safe = False
        elif path.exists() and not path.is_file():
            errors.append(f".aodocs/{name}: metadata must be a regular file")
            safe = False
    return safe


def validate(target: Path) -> list[str]:
    """Return validation errors for *target*; an empty list means success."""

    errors: list[str] = []
    try:
        root = Path(target)
        if not _metadata_preflight(root, errors):
            return errors
        project = _load_json(root / ".aodocs" / "project.json", ".aodocs/project.json", errors)
        documents = _load_json(
            root / ".aodocs" / "documents.json", ".aodocs/documents.json", errors
        )
        manifest = _load_json(
            root / ".aodocs" / "manifest.json", ".aodocs/manifest.json", errors
        )
        platforms, planned_only = (
            _validate_project(project, errors) if project is not None else (set(), set())
        )
        records, by_id, document_paths = (
            _validate_records(documents, root, platforms, planned_only, errors)
            if documents is not None
            else ([], {}, [])
        )
        _validate_relationships(records, by_id, errors)
        if manifest is not None:
            _validate_manifest(root, manifest, errors)
        _validate_links(root, document_paths, errors)
    except Exception as exc:  # A malformed project must never expose a traceback to callers.
        errors.append(f"validation failed safely: {type(exc).__name__}: {exc}")
    return errors
