import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from aodocs_install import install


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        base = Path(self.temp_dir.name)
        self.source = base / "source"
        self.target = base / "project"
        self.source.mkdir()
        self.target.mkdir()
        self.write_source({
            "VERSION": b"1.3.0\n",
            "README.md": b"kit readme\n",
            "RULES/common.md": b"rules\n",
        })

    def write_source(self, files):
        for relative, contents in files.items():
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
        manifest = {"schema_version": 1, "files": list(files)}
        (self.source / "kit-files.json").write_text(json.dumps(manifest), encoding="utf-8")

    def apply(self, profiles=None):
        return install(self.source, self.target, profiles or [], apply=True)

    def manifest(self):
        return json.loads((self.target / ".aodocs/manifest.json").read_text(encoding="utf-8"))

    def test_dry_run_reports_actions_without_writing(self):
        actions = install(self.source, self.target, ["server", "ios"], apply=False)

        self.assertTrue(actions)
        self.assertFalse((self.target / ".aodocs").exists())

    def test_first_install_writes_namespaced_payload_and_metadata(self):
        self.apply(["server", "ios"])

        self.assertEqual(b"kit readme\n", (self.target / ".aodocs/kit/README.md").read_bytes())
        manifest = self.manifest()
        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual("1.3.0", manifest["kit_version"])
        self.assertEqual(
            hashlib.sha256(b"rules\n").hexdigest(), manifest["files"]["RULES/common.md"]
        )
        self.assertEqual(
            {
                "schema_version": 1,
                "project_id": self.target.name,
                "platforms": ["server", "ios"],
                "planned_platforms": [],
            },
            json.loads((self.target / ".aodocs/project.json").read_text(encoding="utf-8")),
        )
        self.assertEqual(
            {"schema_version": 1, "documents": []},
            json.loads((self.target / ".aodocs/documents.json").read_text(encoding="utf-8")),
        )

    def test_empty_profiles_default_to_server(self):
        self.apply([])
        project = json.loads((self.target / ".aodocs/project.json").read_text(encoding="utf-8"))
        self.assertEqual(["server"], project["platforms"])

    def test_dot_target_uses_resolved_directory_name_as_project_id(self):
        previous = Path.cwd()
        try:
            os.chdir(self.target)
            install(self.source, Path("."), [], apply=True)
        finally:
            os.chdir(previous)

        project = json.loads((self.target / ".aodocs/project.json").read_text(encoding="utf-8"))
        self.assertEqual(self.target.name, project["project_id"])

    def test_filesystem_root_target_is_rejected_instead_of_creating_blank_project_id(self):
        filesystem_root = Path(self.target.anchor)
        with self.assertRaisesRegex(ValueError, "non-empty name"):
            install(self.source, filesystem_root, [], apply=False)

    def test_duplicate_profiles_are_deduplicated_preserving_order(self):
        self.apply(["ios", "server", "ios", "web", "server"])
        project = json.loads((self.target / ".aodocs/project.json").read_text(encoding="utf-8"))
        self.assertEqual(["ios", "server", "web"], project["platforms"])

    def test_second_apply_is_idempotent(self):
        self.apply()
        before = {
            path.relative_to(self.target): path.read_bytes()
            for path in self.target.rglob("*") if path.is_file()
        }

        self.apply()

        after = {
            path.relative_to(self.target): path.read_bytes()
            for path in self.target.rglob("*") if path.is_file()
        }
        self.assertEqual(before, after)

    def test_preserves_legacy_root_files_and_existing_user_metadata(self):
        legacy = {
            "AGENTS.md": b"local agents\n",
            "RULES/local.md": b"local rules\n",
            ".aodocs_version": b"1.2.0\n",
            "WRK_existing.md": b"work\n",
        }
        for relative, contents in legacy.items():
            path = self.target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
        aodocs = self.target / ".aodocs"
        aodocs.mkdir()
        project = {"schema_version": 1, "project_id": "custom", "platforms": ["web"], "planned_platforms": ["ios"]}
        documents = {"schema_version": 1, "documents": [{"id": "WRK-1"}]}
        (aodocs / "project.json").write_text(json.dumps(project), encoding="utf-8")
        (aodocs / "documents.json").write_text(json.dumps(documents), encoding="utf-8")

        self.apply(["android"])

        for relative, contents in legacy.items():
            self.assertEqual(contents, (self.target / relative).read_bytes())
        self.assertEqual(project, json.loads((aodocs / "project.json").read_text(encoding="utf-8")))
        self.assertEqual(documents, json.loads((aodocs / "documents.json").read_text(encoding="utf-8")))

    def test_upgrade_replaces_clean_managed_file_and_updates_manifest(self):
        self.apply()
        self.write_source({"VERSION": b"1.3.1\n", "README.md": b"new readme\n", "RULES/common.md": b"rules\n"})

        self.apply()

        self.assertEqual(b"new readme\n", (self.target / ".aodocs/kit/README.md").read_bytes())
        self.assertEqual("1.3.1", self.manifest()["kit_version"])

    def test_modified_managed_file_refuses_without_partial_writes(self):
        self.apply()
        managed = self.target / ".aodocs/kit/README.md"
        managed.write_bytes(b"locally modified\n")
        self.write_source({"VERSION": b"1.3.1\n", "README.md": b"new readme\n", "RULES/common.md": b"new rules\n"})

        with self.assertRaises(ValueError):
            self.apply()

        self.assertEqual(b"locally modified\n", managed.read_bytes())
        self.assertEqual(b"rules\n", (self.target / ".aodocs/kit/RULES/common.md").read_bytes())
        self.assertEqual("1.3.0", self.manifest()["kit_version"])

    def test_blocking_parent_file_refuses_before_any_payload_write(self):
        kit = self.target / ".aodocs/kit"
        kit.mkdir(parents=True)
        (kit / "RULES").write_bytes(b"not a directory\n")

        with self.assertRaises(ValueError):
            self.apply()

        self.assertFalse((kit / "VERSION").exists())
        self.assertFalse((kit / "README.md").exists())

    def test_dirty_managed_file_refuses_even_when_new_source_has_same_bytes(self):
        self.apply()
        managed = self.target / ".aodocs/kit/README.md"
        managed.write_bytes(b"future bytes\n")
        self.write_source({"VERSION": b"1.3.1\n", "README.md": b"future bytes\n", "RULES/common.md": b"rules\n"})

        with self.assertRaises(ValueError):
            self.apply()

    def test_unowned_existing_payload_accepts_only_identical_bytes(self):
        path = self.target / ".aodocs/kit/README.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"kit readme\n")
        self.apply()
        self.assertEqual(b"kit readme\n", path.read_bytes())

        other = Path(self.temp_dir.name) / "other"
        other.mkdir()
        (other / ".aodocs/kit/README.md").mkdir(parents=True)
        (other / ".aodocs/kit/README.md").rmdir()
        (other / ".aodocs/kit/README.md").write_bytes(b"different\n")
        with self.assertRaises(ValueError):
            install(self.source, other, [], apply=True)

    def test_removed_managed_payload_refuses_upgrade_instead_of_deleting(self):
        self.apply()
        self.write_source({"VERSION": b"1.3.1\n", "README.md": b"new readme\n"})

        with self.assertRaises(ValueError):
            self.apply()

        self.assertTrue((self.target / ".aodocs/kit/RULES/common.md").exists())

    def test_rejects_downgrade_before_writing(self):
        self.apply()
        self.write_source({"VERSION": b"1.2.9\n", "README.md": b"older readme\n", "RULES/common.md": b"older rules\n"})

        with self.assertRaises(ValueError):
            self.apply()

        self.assertEqual(b"kit readme\n", (self.target / ".aodocs/kit/README.md").read_bytes())
        self.assertEqual("1.3.0", self.manifest()["kit_version"])

    def test_rejects_malformed_existing_manifest_version_before_writing(self):
        self.apply()
        manifest = self.manifest()
        manifest["kit_version"] = "release-1.3"
        (self.target / ".aodocs/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.write_source({"VERSION": b"1.3.1\n", "README.md": b"new readme\n", "RULES/common.md": b"new rules\n"})

        with self.assertRaises(ValueError):
            self.apply()

        self.assertEqual(b"kit readme\n", (self.target / ".aodocs/kit/README.md").read_bytes())
        self.assertEqual(b"rules\n", (self.target / ".aodocs/kit/RULES/common.md").read_bytes())

    def test_rejects_invalid_profiles_before_writing(self):
        with self.assertRaises(ValueError):
            self.apply(["desktop"])
        self.assertFalse((self.target / ".aodocs").exists())

    def test_rejects_missing_target_and_source_target_overlap(self):
        missing = Path(self.temp_dir.name) / "missing"
        with self.assertRaises(OSError):
            install(self.source, missing, [], apply=False)
        with self.assertRaises(ValueError):
            install(self.source, self.source, [], apply=False)
        nested = self.source / "nested-target"
        nested.mkdir()
        with self.assertRaises(ValueError):
            install(self.source, nested, [], apply=False)

    def test_rejects_invalid_payload_manifests(self):
        invalid_lists = [
            ["VERSION", "README.md", "README.md"],
            ["VERSION", "/absolute.md"],
            ["VERSION", "../escape.md"],
            ["VERSION", "folder/../../escape.md"],
            ["VERSION", "C:/drive.md"],
            ["VERSION", "README.md:stream"],
        ]
        for files in invalid_lists:
            with self.subTest(files=files):
                (self.source / "kit-files.json").write_text(
                    json.dumps({"schema_version": 1, "files": files}), encoding="utf-8"
                )
                with self.assertRaises(ValueError):
                    install(self.source, self.target, [], apply=False)
        (self.source / "kit-files.json").write_text(
            json.dumps({"schema_version": 2, "files": ["README.md"]}), encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            install(self.source, self.target, [], apply=False)

    def test_schema_version_boolean_is_rejected(self):
        (self.source / "kit-files.json").write_text(
            json.dumps({"schema_version": True, "files": ["VERSION"]}), encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            install(self.source, self.target, [], apply=False)

        self.write_source({"VERSION": b"1.3.0\n"})
        self.apply()
        manifest = self.manifest()
        manifest["schema_version"] = True
        (self.target / ".aodocs/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.apply()

    def test_version_must_be_numeric_x_y_z(self):
        for invalid in (b"1.3\n", b"v1.3.0\n", b"1.3.0-beta\n", b"1.a.0\n"):
            with self.subTest(version=invalid):
                self.write_source({"VERSION": invalid, "README.md": b"kit readme\n"})
                with self.assertRaises(ValueError):
                    install(self.source, self.target, [], apply=True)
                self.assertFalse((self.target / ".aodocs").exists())

    def test_rejects_source_symlink_and_target_managed_symlinks(self):
        real = self.source / "real.md"
        real.write_bytes(b"real\n")
        linked = self.source / "linked.md"
        linked.symlink_to(real)
        (self.source / "kit-files.json").write_text(
            json.dumps({"schema_version": 1, "files": ["VERSION", "linked.md"]}), encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            install(self.source, self.target, [], apply=False)

        self.write_source({"VERSION": b"1.3.0\n", "README.md": b"kit readme\n"})
        outside = Path(self.temp_dir.name) / "outside"
        outside.mkdir()
        (self.target / ".aodocs").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            install(self.source, self.target, [], apply=True)
        self.assertEqual([], list(outside.iterdir()))

    def test_accepts_symlink_ancestors_above_source_and_target_roots(self):
        base = Path(self.temp_dir.name)
        alias = base / "alias"
        alias.symlink_to(base, target_is_directory=True)
        other_target = base / "other-project"
        other_target.mkdir()

        install(self.source, alias / self.target.name, [], apply=True)
        install(alias / self.source.name, other_target, [], apply=True)

        self.assertTrue((self.target / ".aodocs/manifest.json").is_file())
        self.assertTrue((other_target / ".aodocs/manifest.json").is_file())

    def test_rejects_source_or_target_root_when_argument_itself_is_symlink(self):
        base = Path(self.temp_dir.name)
        source_alias = base / "source-alias"
        target_alias = base / "target-alias"
        source_alias.symlink_to(self.source, target_is_directory=True)
        target_alias.symlink_to(self.target, target_is_directory=True)

        with self.assertRaises(ValueError):
            install(source_alias, self.target, [], apply=False)
        with self.assertRaises(ValueError):
            install(self.source, target_alias, [], apply=False)

    def test_same_version_still_checks_managed_hashes(self):
        self.apply()
        (self.target / ".aodocs/kit/README.md").write_bytes(b"tampered\n")

        with self.assertRaises(ValueError):
            self.apply()


if __name__ == "__main__":
    unittest.main()
