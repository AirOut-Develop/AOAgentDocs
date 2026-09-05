import importlib.util
import hashlib
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

    def test_session_handoff_rule_and_status_template_are_distributed(self):
        files = set(json.loads((ROOT / "kit-files.json").read_text())["files"])
        self.assertIn("RULES/COMMON/SESSION_HANDOFF.md", files)
        self.assertIn("examples/lifecycle/STATUS.md", files)
        rule = (ROOT / "RULES/COMMON/SESSION_HANDOFF.md").read_text()
        template = (ROOT / "examples/lifecycle/STATUS.md").read_text()
        self.assertIn("docs/STATUS.md", rule)
        self.assertIn("registry", rule)
        self.assertIn("다음 행동", rule)
        self.assertIn("상태 정본", template)
        self.assertIn("0건", template)
        self.assertIn("미검증", template)

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

    def test_git_autocrlf_roundtrip_preserves_installed_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "consumer"
            target.mkdir()
            subprocess.run(["git", "init", "-q", str(target)], check=True)
            subprocess.run(["git", "config", "core.autocrlf", "true"], cwd=target, check=True)
            cli = ROOT / "scripts/aodocs.py"
            result = subprocess.run([sys.executable, str(cli), "install", str(target), "--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

            subprocess.run(["git", "add", "."], cwd=target, check=True, capture_output=True)
            check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=target, capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout)
            manifest = json.loads((target / ".aodocs/manifest.json").read_text())
            for path in manifest["files"]:
                name = ".aodocs/kit/" + path
                staged = subprocess.check_output(["git", "show", ":" + name], cwd=target)
                self.assertEqual(staged, (target / name).read_bytes(), name)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], cwd=target, check=True)
            clone = Path(tmp) / "checkout"
            subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(target), str(clone)], check=True)
            result = subprocess.run([sys.executable, str(clone / ".aodocs/kit/scripts/aodocs.py"), "validate", str(clone)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_published_130_autocrlf_checkout_upgrades_without_losing_edits(self):
        legacy_zip = ROOT / "tests/fixtures/AOAgentDocs_v1.3.0.zip"
        self.assertEqual(hashlib.sha256(legacy_zip.read_bytes()).hexdigest(),
                         "afcd1987981e3678ae4f96d57d345d08e78f16973c628962148469b95d689319")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with zipfile.ZipFile(legacy_zip) as z:
                z.extractall(tmp / "old")
            old_cli = tmp / "old/AOAgentDocs/scripts/aodocs.py"
            target = tmp / "consumer"
            target.mkdir()
            subprocess.run(["git", "init", "-q", str(target)], check=True)
            result = subprocess.run([sys.executable, str(old_cli), "install", str(target), "--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            subprocess.run(["git", "add", "."], cwd=target, check=True, capture_output=True)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "legacy fixture"], cwd=target, check=True)
            checkout = tmp / "checkout"
            subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(target), str(checkout)], check=True)
            cli = ROOT / "scripts/aodocs.py"
            before = (checkout / ".aodocs/kit/VERSION").read_bytes()
            self.assertIn(b"\r\n", before)
            result = subprocess.run([sys.executable, str(cli), "install", str(checkout)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("repair line endings", result.stdout)
            self.assertEqual((checkout / ".aodocs/kit/VERSION").read_bytes(), before)
            result = subprocess.run([sys.executable, str(cli), "install", str(checkout), "--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            subprocess.run(["git", "add", "."], cwd=checkout, check=True, capture_output=True)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "upgrade fixture"], cwd=checkout, check=True)
            final = tmp / "final"
            subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(checkout), str(final)], check=True)
            result = subprocess.run([sys.executable, str(final / ".aodocs/kit/scripts/aodocs.py"), "validate", str(final)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)



if __name__ == "__main__":
    unittest.main()
