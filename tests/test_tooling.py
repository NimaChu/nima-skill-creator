from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from init_skill import init_skill  # noqa: E402
from install_skill import install_skill  # noqa: E402
from package_skill import package_skill  # noqa: E402
from validate_skill import validate_skill_report  # noqa: E402


VALID_SKILL = """---
name: sample-skill
description: Review sample files when users ask for a structured quality check.
license: MIT
compatibility: Requires Python 3.10+
metadata:
  author: test
  version: "1.0"
allowed-tools: Read
---

# Sample Skill

Review the input and return findings.
"""


class ToolingTests(unittest.TestCase):
    def make_skill(self, parent: Path, name: str = "sample-skill") -> Path:
        parent.mkdir(parents=True, exist_ok=True)
        skill_dir = parent / name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            VALID_SKILL.replace("name: sample-skill", f"name: {name}"),
            encoding="utf-8",
        )
        return skill_dir

    def test_validator_accepts_open_standard_optional_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill_dir = self.make_skill(Path(temp))
            report = validate_skill_report(skill_dir)
            self.assertEqual([], report.errors)

    def test_validator_warns_on_product_extension_and_strict_mode_rejects(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill_dir = self.make_skill(Path(temp))
            path = skill_dir / "SKILL.md"
            path.write_text(path.read_text().replace("allowed-tools: Read", "context: fork"), encoding="utf-8")
            normal = validate_skill_report(skill_dir)
            strict = validate_skill_report(skill_dir, strict=True)
            self.assertFalse(normal.errors)
            self.assertTrue(any("context" in warning for warning in normal.warnings))
            self.assertTrue(any("context" in error for error in strict.errors))

    def test_init_is_portable_by_default_and_adapter_is_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            portable = init_skill(
                skill_name="Portable Demo",
                output_dir=root,
                resources=["references"],
                include_examples=True,
                adapters=[],
                interface_overrides=[],
                description="Create portable demos when users ask for a reusable example.",
                license_name="MIT",
                compatibility=None,
                metadata={"author": "test"},
            )
            self.assertFalse((portable / "agents" / "openai.yaml").exists())
            self.assertTrue(validate_skill_report(portable).ok)

            adapted = init_skill(
                skill_name="openai-demo",
                output_dir=root,
                resources=[],
                include_examples=False,
                adapters=["openai"],
                interface_overrides=[],
                description="Create OpenAI adapter demos when users request one.",
                license_name=None,
                compatibility=None,
                metadata={},
            )
            self.assertTrue((adapted / "agents" / "openai.yaml").exists())

    def test_package_excludes_repository_files_and_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = self.make_skill(root)
            (skill_dir / "README.md").write_text("repo docs", encoding="utf-8")
            (skill_dir / "tests").mkdir()
            (skill_dir / "tests" / "test_dummy.py").write_text("pass", encoding="utf-8")
            (skill_dir / "scripts").mkdir()
            script = skill_dir / "scripts" / "run.py"
            script.write_text("print('ok')\n", encoding="utf-8")
            script.chmod(0o755)

            archive = package_skill(skill_dir, root / "dist")
            first = archive.read_bytes()
            second = package_skill(skill_dir, root / "dist").read_bytes()
            self.assertEqual(first, second)
            with ZipFile(archive) as zf:
                names = set(zf.namelist())
            self.assertIn("SKILL.md", names)
            self.assertIn("scripts/run.py", names)
            self.assertNotIn("README.md", names)
            self.assertNotIn("tests/test_dummy.py", names)

    def test_install_directory_and_archive_to_project_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = self.make_skill(root / "source")
            project = root / "project"
            (skill_dir / "README.md").write_text("repo-only", encoding="utf-8")
            installed = install_skill(
                source=skill_dir,
                target="opencode",
                scope="project",
                project_root=project,
            )
            self.assertEqual(project / ".opencode" / "skills" / "sample-skill", installed)
            self.assertTrue((installed / "SKILL.md").exists())
            self.assertFalse((installed / "README.md").exists())

            archive = package_skill(skill_dir, root / "dist")
            custom_root = root / "custom"
            installed_from_zip = install_skill(
                source=archive,
                target="agent",
                scope="user",
                destination=custom_root,
            )
            self.assertEqual(custom_root / "sample-skill", installed_from_zip)
            self.assertTrue((installed_from_zip / "SKILL.md").exists())

    def test_validator_supports_multiline_description_and_nested_extension_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill_dir = Path(temp) / "nested-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                """---
name: nested-skill
description: >-
  Review nested metadata examples when users test
  product-specific skill extensions.
metadata:
  openclaw:
    requires:
      bins: [git]
---

# Nested Skill

Review the input.
""",
                encoding="utf-8",
            )
            normal = validate_skill_report(skill_dir)
            strict = validate_skill_report(skill_dir, strict=True)
            self.assertFalse(normal.errors)
            self.assertTrue(any("metadata" in warning for warning in normal.warnings))
            self.assertTrue(any("metadata" in error for error in strict.errors))


if __name__ == "__main__":
    unittest.main()
