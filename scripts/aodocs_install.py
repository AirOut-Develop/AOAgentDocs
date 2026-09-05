"""Non-destructive installer for the namespaced AOAgentDocs kit."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any


_ALLOWED_PROFILES = {"server", "ios", "android", "web"}
_SCHEMA_VERSION = 1
_VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid JSON: {path}") from error


def _relative_payload(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"invalid payload path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"invalid payload path: {value!r}")
    return value


def _parse_version(value: Any, label: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or _VERSION_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a numeric x.y.z version")
    major, minor, patch = value.split(".")
    return int(major), int(minor), int(patch)


def _assert_no_symlink_components(root: Path, relative: str = "") -> None:
    current = root
    paths = [current]
    if relative:
        for part in PurePosixPath(relative).parts:
            current = current / part
            paths.append(current)
    for path in paths:
        try:
            path.lstat()
        except FileNotFoundError:
            continue
        except NotADirectoryError as error:
            raise ValueError(f"path component is not a directory: {path}") from error
        if os.path.islink(path):
            raise ValueError(f"symlink path is not allowed: {path}")


def _load_payload(source: Path) -> tuple[list[str], dict[str, bytes], str]:
    _assert_no_symlink_components(source, "kit-files.json")
    index_path = source / "kit-files.json"
    if not index_path.is_file():
        raise OSError(f"missing kit-files.json: {index_path}")
    index = _read_json(index_path)
    if not isinstance(index, dict) or type(index.get("schema_version")) is not int or index["schema_version"] != _SCHEMA_VERSION:
        raise ValueError("kit-files.json must use schema_version 1")
    raw_files = index.get("files")
    if not isinstance(raw_files, list):
        raise ValueError("kit-files.json files must be a list")

    files = [_relative_payload(value) for value in raw_files]
    if len(files) != len(set(files)):
        raise ValueError("kit-files.json contains duplicate paths")
    if "VERSION" not in files:
        raise ValueError("kit-files.json must include VERSION")

    contents: dict[str, bytes] = {}
    for relative in files:
        _assert_no_symlink_components(source, relative)
        path = source.joinpath(*PurePosixPath(relative).parts)
        if not path.is_file():
            raise OSError(f"payload file does not exist: {path}")
        contents[relative] = path.read_bytes()

    try:
        version = contents["VERSION"].decode("utf-8").strip()
    except UnicodeDecodeError as error:
        raise ValueError("VERSION must be UTF-8 text") from error
    if not version:
        raise ValueError("VERSION must not be empty")
    _parse_version(version, "VERSION")
    return files, contents, version


def _load_existing_manifest(path: Path) -> tuple[dict[str, str], tuple[int, int, int]] | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"managed path is not a file: {path}")
    manifest = _read_json(path)
    if (
        not isinstance(manifest, dict)
        or type(manifest.get("schema_version")) is not int
        or manifest["schema_version"] != _SCHEMA_VERSION
    ):
        raise ValueError("existing manifest must use schema_version 1")
    installed_version = _parse_version(manifest.get("kit_version"), "existing manifest kit_version")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("existing manifest files must be an object")
    validated: dict[str, str] = {}
    for raw_relative, digest in files.items():
        relative = _relative_payload(raw_relative)
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"invalid manifest hash for {relative}")
        try:
            int(digest, 16)
        except ValueError as error:
            raise ValueError(f"invalid manifest hash for {relative}") from error
        validated[relative] = digest.lower()
    return validated, installed_version


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def install(source: Path, target: Path, profiles: list[str], apply: bool) -> list[str]:
    """Plan or install an AOAgentDocs payload beneath ``target/.aodocs``.

    Validation and conflict detection are completed before any writes. Expected
    input or conflict failures use ``ValueError``; filesystem failures propagate
    as ``OSError``.
    """

    source = Path(source)
    target = Path(target)
    if not source.exists() or not source.is_dir():
        raise OSError(f"source directory does not exist: {source}")
    if not target.exists() or not target.is_dir():
        raise OSError(f"target directory does not exist: {target}")
    _assert_no_symlink_components(source)
    _assert_no_symlink_components(target)

    source_real = source.resolve(strict=True)
    target_real = target.resolve(strict=True)
    if source_real == target_real or source_real in target_real.parents or target_real in source_real.parents:
        raise ValueError("source and target must not overlap")

    selected_profiles = list(profiles) if profiles else ["server"]
    if any(not isinstance(profile, str) or profile not in _ALLOWED_PROFILES for profile in selected_profiles):
        raise ValueError("profiles must be server, ios, android, or web")
    selected_profiles = list(dict.fromkeys(selected_profiles))

    files, source_contents, version = _load_payload(source)
    aodocs = target / ".aodocs"
    kit = aodocs / "kit"
    manifest_path = aodocs / "manifest.json"
    project_path = aodocs / "project.json"
    documents_path = aodocs / "documents.json"

    for relative in (".aodocs", ".aodocs/kit", ".aodocs/manifest.json", ".aodocs/project.json", ".aodocs/documents.json"):
        _assert_no_symlink_components(target, relative)
    old_manifest = _load_existing_manifest(manifest_path)
    old_files, installed_version = old_manifest if old_manifest is not None else ({}, None)
    if installed_version is not None and _parse_version(version, "VERSION") < installed_version:
        raise ValueError("kit downgrade is not allowed")

    removed = sorted(set(old_files) - set(files))
    if removed:
        raise ValueError(f"installed managed files are absent from the new payload: {', '.join(removed)}")

    desired_hashes = {relative: _sha256(source_contents[relative]) for relative in files}
    actions: list[str] = []
    for relative in files:
        managed_relative = f".aodocs/kit/{relative}"
        _assert_no_symlink_components(target, managed_relative)
        destination = kit.joinpath(*PurePosixPath(relative).parts)
        if destination.exists():
            if not destination.is_file():
                raise ValueError(f"managed path is not a file: {destination}")
            existing = destination.read_bytes()
            if relative in old_files:
                if _sha256(existing) != old_files[relative]:
                    raise ValueError(f"managed file was locally modified: {relative}")
            elif existing != source_contents[relative]:
                raise ValueError(f"unowned file conflicts with payload: {relative}")
            if existing != source_contents[relative]:
                actions.append(f"update {managed_relative}")
        else:
            if relative in old_files:
                raise ValueError(f"managed file is missing: {relative}")
            actions.append(f"create {managed_relative}")

    project = {
        "schema_version": _SCHEMA_VERSION,
        "project_id": target.name,
        "platforms": selected_profiles,
        "planned_platforms": [],
    }
    documents = {"schema_version": _SCHEMA_VERSION, "documents": []}
    for path, label in ((project_path, ".aodocs/project.json"), (documents_path, ".aodocs/documents.json")):
        if path.exists() and not path.is_file():
            raise ValueError(f"managed metadata path is not a file: {path}")
        if not path.exists():
            actions.append(f"create {label}")

    new_manifest = {
        "schema_version": _SCHEMA_VERSION,
        "kit_version": version,
        "files": desired_hashes,
    }
    manifest_bytes = _json_bytes(new_manifest)
    if not manifest_path.exists() or manifest_path.read_bytes() != manifest_bytes:
        actions.append("create .aodocs/manifest.json" if not manifest_path.exists() else "update .aodocs/manifest.json")

    if not apply:
        return actions

    kit.mkdir(parents=True, exist_ok=True)
    for relative in files:
        destination = kit.joinpath(*PurePosixPath(relative).parts)
        desired = source_contents[relative]
        if not destination.exists() or destination.read_bytes() != desired:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(desired)
    if not project_path.exists():
        project_path.write_bytes(_json_bytes(project))
    if not documents_path.exists():
        documents_path.write_bytes(_json_bytes(documents))
    if not manifest_path.exists() or manifest_path.read_bytes() != manifest_bytes:
        manifest_path.write_bytes(manifest_bytes)
    return actions


__all__ = ["install"]
