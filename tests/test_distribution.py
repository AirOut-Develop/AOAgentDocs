import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def packager(self):
        spec = importlib.util.spec_from_file_location("release_package", ROOT / "scripts/release_package.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build_package

    def fixture(self, root):
        (root / "VERSION").write_text("1.3.0\n")
        (root / "README.md").write_text("# Kit\n")
        (root / "kit-files.json").write_text(json.dumps({
            "schema_version": 1, "files": ["VERSION", "README.md", "kit-files.json"]}))

    def test_explicit_payload_excludes_local_private_files_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / ".env").write_text("SECRET=not-for-package")
            (root / "private-notes.md").write_text("not-for-package")
            output = self.packager()(root)
            before = output.read_bytes()
            self.assertEqual(self.packager()(root).read_bytes(), before)
            with zipfile.ZipFile(output) as z:
                self.assertEqual(set(z.namelist()), {
                    "AOAgentDocs/VERSION", "AOAgentDocs/README.md", "AOAgentDocs/kit-files.json"})

    def test_manifest_schema_bool_and_non_ascii_versions_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            manifest = json.loads((root / "kit-files.json").read_text())
            manifest["schema_version"] = True
            (root / "kit-files.json").write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                self.packager()(root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / "VERSION").write_text("١.٣.٠\n")
            with self.assertRaises(ValueError):
                self.packager()(root)

    def test_unsafe_missing_duplicate_and_symlink_payloads_are_rejected(self):
        for bad in ["../secret", "/etc/passwd", ".env", "notes.md", "scripts/missing.py"]:
            with self.subTest(path=bad), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.fixture(root)
                manifest = {"schema_version": 1, "files": ["VERSION", bad]}
                (root / "kit-files.json").write_text(json.dumps(manifest))
                with self.assertRaises((ValueError, FileNotFoundError)):
                    self.packager()(root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / "README.md").unlink()
            (root / "README.md").symlink_to(root / "VERSION")
            with self.assertRaises(ValueError):
                self.packager()(root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / "kit-files.json").write_text(json.dumps({"schema_version": 1, "files": ["VERSION", "VERSION"]}))
            with self.assertRaises(ValueError):
                self.packager()(root)

    def test_zip_installs_validates_and_preserves_host_project(self):
        output = self.packager()(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with zipfile.ZipFile(output) as z:
                z.extractall(tmp / "unpacked")
            cli = tmp / "unpacked/AOAgentDocs/scripts/aodocs.py"
            target = tmp / "consumer"
            target.mkdir()
            existing = {"README.md": "project readme", "AGENTS.md": "project rules", ".aodocs_version": "1.2.0"}
            for name, value in existing.items():
                (target / name).write_text(value)
            base = [sys.executable, str(cli)]
            result = subprocess.run(base + ["install", str(target), "--profile", "server", "--profile", "ios"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / ".aodocs").exists())
            for _ in range(2):
                result = subprocess.run(base + ["install", str(target), "--profile", "server", "--profile", "ios", "--apply"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run([sys.executable, str(target / ".aodocs/kit/scripts/aodocs.py"), "validate", str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            for name, value in existing.items():
                self.assertEqual((target / name).read_text(), value)

    def test_payload_markdown_links_and_versions_are_consistent(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from aodocs_validate import _validate_links
            files = json.loads((ROOT / "kit-files.json").read_text())["files"]
            errors = []
            _validate_links(ROOT, [ROOT / f for f in files if f.endswith(".md")], errors)
            self.assertEqual(errors, [])
        finally:
            sys.path.pop(0)
        version = (ROOT / "VERSION").read_text().strip()
        for name in ("README.md", "CHANGELOG.md", "ROADMAP.md"):
            self.assertIn(version, (ROOT / name).read_text(), name)
        self.assertIn(f"git clone --branch aodocs/v{version} --depth 1", (ROOT / "README.md").read_text())

    def test_documented_templates_register_without_claiming_product_success(self):
        self.packager()(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            target.mkdir()
            cli = ROOT / "scripts/aodocs.py"
            result = subprocess.run([sys.executable, str(cli), "install", str(target), "--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for source, destination in (("PRD.md", "prd"), ("PLAN.md", "plans"), ("VERIFICATION.md", "verification")):
                path = target / "docs" / destination / "example.md"
                path.parent.mkdir(parents=True)
                path.write_bytes((ROOT / "examples/lifecycle" / source).read_bytes())
            data = (ROOT / "examples/lifecycle/documents.example.json").read_bytes()
            (target / ".aodocs/documents.json").write_bytes(data)
            result = subprocess.run([sys.executable, str(cli), "validate", str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Product tests were NOT executed", result.stdout)


if __name__ == "__main__":
    unittest.main()
