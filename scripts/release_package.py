#!/usr/bin/env python3
"""Build the explicit public kit payload, independent of shell/platform."""
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT_FILES = {"VERSION", "README.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE",
              "RELEASE_POLICY.md", "ROADMAP.md", "MIGRATION_PROMPT.txt", "UPGRADE_PROMPT.txt",
              "kit-files.json", "AGENT_AUDIT_PROMPT.md"}


def build_package(root: Path) -> Path:
    root = root.resolve()
    manifest_path = root / "kit-files.json"
    if manifest_path.is_symlink():
        raise ValueError("symlink kit-files.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("invalid kit-files manifest")
    files = manifest.get("files")
    if (type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1
            or not isinstance(files, list) or not files):
        raise ValueError("invalid kit-files manifest")
    seen = set()
    payload = {}
    for name in files:
        if not isinstance(name, str):
            raise ValueError("payload path must be a string")
        path = PurePosixPath(name)
        if (not name or path.is_absolute() or "\\" in name or ":" in name or
                any(p in (".", "..") or p.startswith(".") for p in name.split("/")) or
                name in seen or str(path) != name):
            raise ValueError(f"unsafe/duplicate payload path: {name}")
        if name not in ROOT_FILES and path.parts[0] not in {"RULES", "examples", "scripts"}:
            raise ValueError(f"not a distributable kit path: {name}")
        if path.suffix not in {".md", ".txt", ".json", ".py", ".sh", ".ps1"} and name not in ROOT_FILES:
            raise ValueError(f"unsupported payload file: {name}")
        current = root
        for part in path.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(f"symlink payload: {name}")
        if not current.is_file():
            raise FileNotFoundError(current)
        payload[name] = current.read_bytes()
        seen.add(name)
    if not {"VERSION", "kit-files.json"}.issubset(payload):
        raise ValueError("VERSION and kit-files.json must be included")
    version = payload["VERSION"].decode("utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("invalid SemVer VERSION")
    dist = root / "dist"
    output = dist / f"AOAgentDocs_v{version}.zip"
    if dist.is_symlink() or output.is_symlink():
        raise ValueError("symlink output")
    dist.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            entry = zipfile.ZipInfo("AOAgentDocs/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    return output


if __name__ == "__main__":
    try:
        print(build_package(Path(__file__).resolve().parents[1]))
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        raise SystemExit(f"ERROR: {error}")
