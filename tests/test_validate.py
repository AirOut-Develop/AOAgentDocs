import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from aodocs_validate import validate


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.target = Path(self.temp.name)
        aodocs = self.target / ".aodocs"
        kit = aodocs / "kit"
        kit.mkdir(parents=True)
        (kit / "VERSION").write_text("1.3.0\n", encoding="utf-8")
        self.write_json(
            ".aodocs/kit/kit-files.json",
            {"schema_version": 1, "files": ["VERSION", "kit-files.json"]},
        )
        self.write_json(
            ".aodocs/manifest.json",
            {
                "schema_version": 1,
                "kit_version": "1.3.0",
                "files": {
                    name: hashlib.sha256((kit / name).read_bytes()).hexdigest()
                    for name in ("VERSION", "kit-files.json")
                },
            },
        )
        self.write_json(
            ".aodocs/project.json",
            {
                "schema_version": 1,
                "project_id": "sample-project",
                "platforms": ["server"],
                "planned_platforms": ["ios"],
            },
        )
        self.write_json(".aodocs/documents.json", {"schema_version": 1, "documents": []})

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, relative, value):
        path = self.target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def write_doc(self, relative, body="# Document\n"):
        path = self.target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    def record(self, doc_id, kind, path, status, **extra):
        result = {
            "id": doc_id,
            "kind": kind,
            "path": path,
            "status": status,
            "revision": 1,
            "owner": "team",
            "platforms": ["server"],
        }
        result.update(extra)
        self.write_doc(path)
        return result

    def set_documents(self, documents):
        self.write_json(
            ".aodocs/documents.json", {"schema_version": 1, "documents": documents}
        )

    def refresh_managed_hash(self, relative):
        manifest_path = self.target / ".aodocs/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][relative] = hashlib.sha256(
            (self.target / ".aodocs/kit" / relative).read_bytes()
        ).hexdigest()
        self.write_json(".aodocs/manifest.json", manifest)

    def assert_error_contains(self, fragment):
        errors = validate(self.target)
        self.assertTrue(errors, "validation unexpectedly succeeded")
        self.assertTrue(
            any(fragment in error for error in errors),
            f"{fragment!r} not found in {errors!r}",
        )

    def test_empty_installed_registry_is_valid(self):
        self.assertEqual([], validate(self.target))

    def test_bad_json_and_wrong_top_level_types_return_errors(self):
        (self.target / ".aodocs/documents.json").write_text("{", encoding="utf-8")
        self.assert_error_contains("documents.json")

        self.write_json(".aodocs/documents.json", [])
        self.assert_error_contains("object")

    def test_varied_malformed_record_fields_do_not_use_generic_exception_fallback(self):
        self.write_doc("docs/bad.md")
        self.set_documents(
            [
                {
                    "id": "DOC-1",
                    "kind": ["prd"],
                    "path": "docs/bad.md",
                    "status": {"draft": True},
                    "revision": "one",
                    "owner": ["team"],
                    "platforms": [{"server": True}],
                    "refs": [["DOC-2"]],
                    "evidence": [{"id": "VER-1"}],
                    "requirements": [{"id": "REQ-1"}],
                    "covers": [{"id": "REQ-1"}],
                }
            ]
        )
        errors = validate(self.target)
        self.assertTrue(errors)
        self.assertFalse(any("validation failed safely" in error for error in errors), errors)
        for field in ("kind", "status", "revision", "owner", "platforms"):
            self.assertTrue(any(field in error for error in errors), (field, errors))

    def test_boolean_schema_versions_are_rejected_in_all_metadata_files(self):
        project = json.loads((self.target / ".aodocs/project.json").read_text())
        documents = json.loads((self.target / ".aodocs/documents.json").read_text())
        manifest = json.loads((self.target / ".aodocs/manifest.json").read_text())
        for value, relative in (
            (project, ".aodocs/project.json"),
            (documents, ".aodocs/documents.json"),
            (manifest, ".aodocs/manifest.json"),
        ):
            value["schema_version"] = True
            self.write_json(relative, value)
        errors = validate(self.target)
        schema_errors = [error for error in errors if "schema_version" in error]
        self.assertEqual(3, len(schema_errors), errors)

    def test_project_schema_and_platforms_are_validated(self):
        self.write_json(
            ".aodocs/project.json",
            {
                "schema_version": 2,
                "project_id": "",
                "platforms": ["desktop"],
                "planned_platforms": "ios",
            },
        )
        errors = validate(self.target)
        self.assertTrue(any("schema_version" in e for e in errors))
        self.assertTrue(any("project_id" in e for e in errors))
        self.assertTrue(any("desktop" in e for e in errors))
        self.assertTrue(any("planned_platforms" in e for e in errors))

    def test_required_record_fields_and_field_types_are_validated(self):
        self.set_documents([{"id": "lower", "revision": 0}])
        errors = validate(self.target)
        for field in ("id", "kind", "path", "status", "revision", "owner", "platforms"):
            self.assertTrue(any(field in e for e in errors), (field, errors))

    def test_duplicate_document_and_requirement_ids_are_rejected(self):
        prd = self.record(
            "PRD-1", "prd", "docs/prd.md", "draft", requirements=["REQ-1", "REQ-1"]
        )
        work = self.record("REQ-1", "work", "docs/work.md", "planned")
        duplicate = self.record("PRD-1", "plan", "docs/plan.md", "planned")
        self.set_documents([prd, work, duplicate])
        errors = validate(self.target)
        self.assertGreaterEqual(sum("duplicate" in e.lower() for e in errors), 2)

    def test_kind_status_matrix_is_enforced(self):
        self.set_documents([self.record("WRK-1", "work", "docs/work.md", "approved")])
        self.assert_error_contains("status")

    def test_document_path_must_be_safe_existing_markdown(self):
        outside = self.target.parent / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        try:
            records = [
                {**self.record("DOC-1", "prd", "docs/ok.md", "draft"), "path": "../outside.md"},
                {**self.record("DOC-2", "prd", "docs/ok2.md", "draft"), "path": "/tmp/a.md"},
                {**self.record("DOC-3", "prd", "docs/ok3.md", "draft"), "path": "docs/no.txt"},
            ]
            self.set_documents(records)
            self.assert_error_contains("path")
        finally:
            outside.unlink(missing_ok=True)

    def test_document_paths_reject_colons_and_non_normalized_aliases(self):
        records = []
        for index, path in enumerate(("docs:name.md", "./docs/name.md", "docs//name.md"), 1):
            record = self.record(f"DOC-{index}", "prd", f"docs/real-{index}.md", "draft")
            record["path"] = path
            records.append(record)
        self.set_documents(records)
        errors = validate(self.target)
        for path in ("docs:name.md", "./docs/name.md", "docs//name.md"):
            self.assertTrue(any("path" in error for error in errors), (path, errors))
        self.assertGreaterEqual(sum("safe project-relative path" in error for error in errors), 3)

    def test_document_path_symlink_is_rejected(self):
        real = self.target / "docs/real.md"
        self.write_doc("docs/real.md")
        (self.target / "docs/link.md").symlink_to(real)
        record = self.record("DOC-1", "prd", "docs/unused.md", "draft")
        record["path"] = "docs/link.md"
        self.set_documents([record])
        self.assert_error_contains("symlink")

    def test_optional_id_arrays_and_record_platforms_are_validated(self):
        record = self.record("DOC-1", "prd", "docs/prd.md", "draft")
        record.update(refs="DOC-2", evidence=[1], requirements=["bad id"], covers=["REQ-X"])
        record["platforms"] = ["android"]
        self.set_documents([record])
        errors = validate(self.target)
        for field in ("refs", "evidence", "requirements", "covers", "android"):
            self.assertTrue(any(field in e for e in errors), (field, errors))

    def test_requirements_are_declared_only_by_prds_and_covers_must_resolve(self):
        plan = self.record(
            "PLAN-1", "plan", "docs/plan.md", "planned", requirements=["REQ-1"], covers=["REQ-X"]
        )
        self.set_documents([plan])
        errors = validate(self.target)
        self.assertTrue(any("requirements" in e and "prd" in e for e in errors))
        self.assertTrue(any("REQ-X" in e for e in errors))

    def test_refs_must_resolve_and_evidence_must_be_verification(self):
        prd = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        work = self.record(
            "WRK-1",
            "work",
            "docs/work.md",
            "in_progress",
            refs=["MISSING"],
            evidence=["PRD-1"],
        )
        self.set_documents([prd, work])
        errors = validate(self.target)
        self.assertTrue(any("MISSING" in e for e in errors))
        self.assertTrue(any("evidence" in e and "verification" in e for e in errors))

    def test_approved_document_requires_matching_complete_approval(self):
        prd = self.record(
            "PRD-1",
            "prd",
            "docs/prd.md",
            "approved",
            revision=2,
            approval={"by": "", "at": "2026-09-05", "revision": 1},
        )
        self.set_documents([prd])
        errors = validate(self.target)
        self.assertTrue(any("approval.by" in e for e in errors))
        self.assertTrue(any("approval.revision" in e for e in errors))

    def test_approval_revision_boolean_does_not_match_integer_revision(self):
        prd = self.record(
            "PRD-1",
            "prd",
            "docs/prd.md",
            "approved",
            revision=1,
            approval={"by": "reviewer", "at": "2026-09-05", "revision": True},
        )
        self.set_documents([prd])
        self.assert_error_contains("approval.revision")

    def test_passed_and_waived_verification_metadata_is_required(self):
        passed = self.record("VER-1", "verification", "docs/v1.md", "passed", command="")
        waived = self.record("VER-2", "verification", "docs/v2.md", "waived", reason="")
        self.set_documents([passed, waived])
        errors = validate(self.target)
        for field in ("command", "environment", "source_revision", "reason", "expires_at"):
            self.assertTrue(any(field in e for e in errors), (field, errors))

    def test_completed_work_requires_passed_verification_covering_its_requirements(self):
        prd = self.record(
            "PRD-1", "prd", "docs/prd.md", "draft", requirements=["REQ-1", "REQ-2"]
        )
        passed = self.record(
            "VER-1",
            "verification",
            "docs/ver.md",
            "passed",
            covers=["REQ-1"],
            command="pytest",
            environment="ci",
            source_revision="abc",
        )
        waived = self.record(
            "VER-2",
            "verification",
            "docs/waived.md",
            "waived",
            covers=["REQ-2"],
            reason="blocked",
            owner="team",
            expires_at="2026-10-01",
        )
        work = self.record(
            "WRK-1",
            "work",
            "docs/work.md",
            "done",
            covers=["REQ-1", "REQ-2"],
            evidence=["VER-1", "VER-2"],
        )
        self.set_documents([prd, passed, waived, work])
        self.assert_error_contains("REQ-2")

    def test_released_release_requires_at_least_one_passed_verification(self):
        waived = self.record(
            "VER-1",
            "verification",
            "docs/waived.md",
            "waived",
            reason="later",
            owner="team",
            expires_at="2026-10-01",
        )
        release = self.record(
            "REL-1", "release", "docs/release.md", "released", evidence=["VER-1"]
        )
        self.set_documents([waived, release])
        self.assert_error_contains("passed verification")

    def test_manifest_version_hash_and_safe_payload_paths_are_validated(self):
        self.write_json(
            ".aodocs/manifest.json",
            {
                "schema_version": 1,
                "kit_version": "9.9.9",
                "files": {"VERSION": "0" * 64, "../escape": "0" * 64},
            },
        )
        errors = validate(self.target)
        self.assertTrue(any("kit_version" in e for e in errors))
        self.assertTrue(any("sha256" in e for e in errors))
        self.assertTrue(any("../escape" in e for e in errors))

    def test_manifest_must_manage_version(self):
        self.write_json(
            ".aodocs/manifest.json",
            {"schema_version": 1, "kit_version": "1.3.0", "files": {}},
        )
        self.assert_error_contains("VERSION")

    def test_symlinked_kit_root_is_rejected(self):
        kit = self.target / ".aodocs/kit"
        external = self.target / "external-kit"
        kit.rename(external)
        kit.symlink_to(external, target_is_directory=True)
        self.assert_error_contains("symlink")

    def test_version_symlink_is_rejected_without_reading_its_external_target(self):
        version = self.target / ".aodocs/kit/VERSION"
        external = self.target / "external-version"
        external.write_bytes(b"\xff")
        version.unlink()
        version.symlink_to(external)
        errors = validate(self.target)
        self.assertTrue(any("VERSION" in error and "symlink" in error for error in errors), errors)
        self.assertFalse(any("cannot read .aodocs/kit/VERSION" in error for error in errors), errors)

    def test_missing_relative_markdown_link_is_reported(self):
        record = self.record(
            "PRD-1", "prd", "docs/prd.md", "draft"
        )
        self.write_doc("docs/prd.md", "[missing](other.md)\n")
        self.set_documents([record])
        self.assert_error_contains("other.md")

    def test_link_validation_ignores_code_external_anchor_and_templates(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc(
            "docs/prd.md",
            """[web](https://example.com/no.md) [anchor](#part) [template]({path}.md)

```md
[code](missing.md)
```
""",
        )
        self.set_documents([record])
        self.assertEqual([], validate(self.target))

    def test_link_validation_ignores_unterminated_fenced_code(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc("docs/prd.md", "```md\n[example](missing.md)\n")
        self.set_documents([record])
        self.assertEqual([], validate(self.target))

    def test_empty_and_malformed_link_destinations_return_useful_errors(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc("docs/prd.md", "[empty]( ) [malformed](http://[)\n")
        self.set_documents([record])
        errors = validate(self.target)
        self.assertTrue(any("link" in error for error in errors), errors)
        self.assertFalse(any("validation failed safely" in error for error in errors), errors)

    def test_active_and_planned_platforms_must_not_overlap(self):
        self.write_json(
            ".aodocs/project.json",
            {
                "schema_version": 1,
                "project_id": "sample-project",
                "platforms": ["server", "ios"],
                "planned_platforms": ["ios", "android"],
            },
        )
        self.assert_error_contains("both active and planned")

    def test_planned_only_platform_cannot_have_completed_lifecycle_records(self):
        self.write_json(
            ".aodocs/project.json",
            {
                "schema_version": 1,
                "project_id": "sample-project",
                "platforms": ["server"],
                "planned_platforms": ["android"],
            },
        )
        records = []
        for doc_id, kind, status in (
            ("VER-1", "verification", "passed"),
            ("WRK-1", "work", "done"),
            ("PLAN-1", "plan", "done"),
            ("ISS-1", "issue", "done"),
            ("REL-1", "release", "released"),
        ):
            extra = {"platforms": ["android"]}
            if kind == "verification":
                extra.update(command="test", environment="ci", source_revision="abc")
            else:
                extra["evidence"] = ["VER-1"]
            records.append(
                self.record(doc_id, kind, f"docs/{doc_id}.md", status, **extra)
            )
        self.set_documents(records)
        errors = validate(self.target)
        for doc_id in ("VER-1", "WRK-1", "PLAN-1", "ISS-1", "REL-1"):
            self.assertTrue(
                any(doc_id in error and "planned-only" in error for error in errors),
                (doc_id, errors),
            )

    def test_planned_only_platform_is_allowed_for_noncompleted_records(self):
        project = json.loads((self.target / ".aodocs/project.json").read_text())
        project["planned_platforms"] = ["android"]
        self.write_json(".aodocs/project.json", project)
        self.set_documents(
            [self.record("PLAN-1", "plan", "docs/plan.md", "planned", platforms=["android"])]
        )
        self.assertEqual([], validate(self.target))

    def test_approved_design_may_describe_a_planned_only_platform(self):
        project = json.loads((self.target / ".aodocs/project.json").read_text())
        project["planned_platforms"] = ["android"]
        self.write_json(".aodocs/project.json", project)
        self.set_documents(
            [
                self.record(
                    "DESIGN-1",
                    "design",
                    "docs/design.md",
                    "approved",
                    platforms=["android"],
                    approval={"by": "reviewer", "at": "2026-09-05", "revision": 1},
                )
            ]
        )
        self.assertEqual([], validate(self.target))

    def test_aodocs_and_metadata_symlinks_are_rejected_before_reads(self):
        with tempfile.TemporaryDirectory() as other_temp:
            other = Path(other_temp)
            aodocs = self.target / ".aodocs"
            moved = other / "external-aodocs"
            aodocs.rename(moved)
            (moved / "project.json").write_bytes(b"\xff")
            aodocs.symlink_to(moved, target_is_directory=True)
            errors = validate(self.target)
            self.assertTrue(any(".aodocs" in error and "symlink" in error for error in errors), errors)
            self.assertFalse(any("invalid JSON" in error or "cannot be read" in error for error in errors), errors)

    def test_metadata_file_symlink_is_rejected_before_read(self):
        project = self.target / ".aodocs/project.json"
        external = self.target / "external-project.json"
        external.write_bytes(b"\xff")
        project.unlink()
        project.symlink_to(external)
        errors = validate(self.target)
        self.assertTrue(any("project.json" in error and "symlink" in error for error in errors), errors)
        self.assertFalse(any("cannot be read" in error for error in errors), errors)

    def test_manifest_keys_must_exactly_match_trusted_kit_file_index(self):
        manifest_path = self.target / ".aodocs/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        payload = self.target / ".aodocs/kit/EXTRA.md"
        payload.write_text("extra", encoding="utf-8")
        manifest["files"]["EXTRA.md"] = hashlib.sha256(payload.read_bytes()).hexdigest()
        self.write_json(".aodocs/manifest.json", manifest)
        self.assert_error_contains("exactly match")

    def test_kit_index_is_parsed_only_after_its_hash_matches(self):
        index = self.target / ".aodocs/kit/kit-files.json"
        index.write_bytes(b"\xff")
        errors = validate(self.target)
        self.assertTrue(any("sha256 mismatch" in error and "kit-files.json" in error for error in errors), errors)
        self.assertFalse(any("kit-files.json: invalid" in error for error in errors), errors)

    def test_trusted_kit_index_rejects_unsafe_duplicate_and_absolute_paths(self):
        for files in (
            ["VERSION", "kit-files.json", "VERSION"],
            ["VERSION", "kit-files.json", "../escape"],
            ["VERSION", "kit-files.json", "/absolute"],
        ):
            with self.subTest(files=files):
                self.write_json(
                    ".aodocs/kit/kit-files.json", {"schema_version": 1, "files": files}
                )
                self.refresh_managed_hash("kit-files.json")
                self.assert_error_contains("kit-files.json")

    def test_manifest_requires_kit_file_index_to_be_managed(self):
        manifest = json.loads((self.target / ".aodocs/manifest.json").read_text())
        del manifest["files"]["kit-files.json"]
        self.write_json(".aodocs/manifest.json", manifest)
        self.assert_error_contains("kit-files.json")

    def test_missing_markdown_reference_definition_target_is_reported(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc("docs/prd.md", "See [the plan][plan].\n\n[plan]: missing.md\n")
        self.set_documents([record])
        self.assert_error_contains("missing.md")

    def test_undefined_named_markdown_reference_is_reported(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc("docs/prd.md", "See [the plan][undefined].\n")
        self.set_documents([record])
        self.assert_error_contains("undefined")

    def test_inline_code_reference_examples_are_ignored_but_adjacent_real_reference_is_checked(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc(
            "docs/prd.md",
            "`[text][fake-one]` and ``![image][fake-two]`` but [real][missing].\n",
        )
        self.set_documents([record])
        errors = validate(self.target)
        self.assertTrue(any("missing" in error for error in errors), errors)
        self.assertFalse(any("fake-one" in error or "fake-two" in error for error in errors), errors)

    def test_missing_inline_image_is_reported(self):
        record = self.record("PRD-1", "prd", "docs/prd.md", "draft")
        self.write_doc("docs/prd.md", "![diagram](missing.png)\n")
        self.set_documents([record])
        self.assert_error_contains("missing.png")


if __name__ == "__main__":
    unittest.main()
