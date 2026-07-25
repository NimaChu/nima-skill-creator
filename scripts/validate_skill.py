#!/usr/bin/env python3
"""Validate an Agent Skills directory against the portable core format."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
RECOMMENDED_MAX_BODY_LINES = 500
STANDARD_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def extract_frontmatter(content: str) -> tuple[str, str]:
    normalized = content.replace("\r\n", "\n")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)(.*)$", normalized, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter.")
    return match.group(1), match.group(2)


def parse_top_level_frontmatter(
    frontmatter: str,
) -> tuple[dict[str, str], dict[str, str], bool]:
    """Parse portable YAML fields without adding a third-party dependency.

    Supports quoted/plain scalars, folded or literal top-level scalar blocks,
    simple string-to-string metadata, and tolerates nested product extensions.
    """

    values: dict[str, str] = {}
    metadata: dict[str, str] = {}
    metadata_is_complex = False
    lines = frontmatter.splitlines()
    index = 0
    active_mapping: str | None = None

    while index < len(lines):
        raw_line = lines[index]
        line_number = index + 1
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            index += 1
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent == 0:
            if ":" not in raw_line:
                raise ValueError(f"Invalid frontmatter line {line_number}: {raw_line}")
            key, raw_value = raw_line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            if not key:
                raise ValueError(f"Empty frontmatter key on line {line_number}.")
            if key in values:
                raise ValueError(f"Duplicate frontmatter key: {key}")

            if value in {">", ">-", ">+", "|", "|-", "|+"}:
                block_lines: list[str] = []
                index += 1
                while index < len(lines):
                    candidate = lines[index]
                    candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                    if candidate.strip() and candidate_indent == 0:
                        break
                    block_lines.append(candidate.strip())
                    index += 1
                separator = "\n" if value.startswith("|") else " "
                values[key] = separator.join(part for part in block_lines if part).strip()
                active_mapping = None
                continue

            values[key] = _strip_yaml_scalar(value)
            active_mapping = key if not value else None
            index += 1
            continue

        if active_mapping == "metadata":
            stripped = raw_line.strip()
            if (
                indent != 2
                or ":" not in stripped
                or stripped.startswith(("{", "[", "-"))
            ):
                metadata_is_complex = True
                index += 1
                continue
            key, raw_value = stripped.split(":", 1)
            key = key.strip().strip("\"'")
            value = raw_value.strip()
            if not key or not value or value in {"{", "[", "|", ">"}:
                metadata_is_complex = True
            else:
                metadata[key] = _strip_yaml_scalar(value)
        index += 1

    return values, metadata, metadata_is_complex


def _strip_yaml_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _validate_links(skill_dir: Path, body: str, report: ValidationReport) -> None:
    for target in LINK_PATTERN.findall(body):
        target = target.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("/"):
            report.warnings.append(f"Absolute link reduces portability: {target}")
            continue
        candidate = (skill_dir / target).resolve()
        try:
            candidate.relative_to(skill_dir.resolve())
        except ValueError:
            report.errors.append(f"Link escapes the skill directory: {target}")
            continue
        if not candidate.exists():
            report.errors.append(f"Referenced file does not exist: {target}")


def validate_skill_report(
    skill_dir: Path, strict: bool = False, require_directory_match: bool = True
) -> ValidationReport:
    report = ValidationReport()
    skill_dir = skill_dir.expanduser().resolve()
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        report.errors.append("SKILL.md not found.")
        return report

    if skill_md.is_symlink():
        report.errors.append("SKILL.md must not be a symlink.")
        return report

    content = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter_text, body = extract_frontmatter(content)
        frontmatter, metadata, metadata_is_complex = parse_top_level_frontmatter(frontmatter_text)
    except Exception as exc:
        report.errors.append(str(exc))
        return report

    unknown_keys = sorted(set(frontmatter) - STANDARD_FRONTMATTER_KEYS)
    if unknown_keys:
        message = "Product-specific or unknown frontmatter keys: " + ", ".join(unknown_keys)
        if strict:
            report.errors.append(message)
        else:
            report.warnings.append(message)

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    compatibility = frontmatter.get("compatibility", "").strip()

    if not name:
        report.errors.append("Frontmatter 'name' is required.")
    elif not NAME_PATTERN.fullmatch(name):
        report.errors.append("Frontmatter 'name' must use lowercase letters, digits, and single hyphens.")
    elif len(name) > MAX_SKILL_NAME_LENGTH:
        report.errors.append(f"Frontmatter 'name' exceeds {MAX_SKILL_NAME_LENGTH} characters.")
    elif require_directory_match and skill_dir.name != name:
        report.errors.append(
            f"Frontmatter name '{name}' must match the parent directory '{skill_dir.name}'."
        )

    if not description:
        report.errors.append("Frontmatter 'description' is required.")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        report.errors.append(
            f"Frontmatter 'description' exceeds {MAX_DESCRIPTION_LENGTH} characters."
        )

    if compatibility and len(compatibility) > MAX_COMPATIBILITY_LENGTH:
        report.errors.append(
            f"Frontmatter 'compatibility' exceeds {MAX_COMPATIBILITY_LENGTH} characters."
        )

    if metadata_is_complex:
        message = "Frontmatter 'metadata' contains nested or non-string values; portability varies by client."
        if strict:
            report.errors.append(message)
        else:
            report.warnings.append(message)
    elif "metadata" in frontmatter and not metadata and not frontmatter.get("metadata"):
        report.warnings.append("Frontmatter 'metadata' is present but empty.")

    if not body.strip():
        report.errors.append("SKILL.md body is empty.")
    body_lines = body.splitlines()
    if len(body_lines) > RECOMMENDED_MAX_BODY_LINES:
        report.warnings.append(
            f"SKILL.md body has {len(body_lines)} lines; keep it under {RECOMMENDED_MAX_BODY_LINES} when practical."
        )

    _validate_links(skill_dir, body, report)

    for path in sorted(skill_dir.rglob("*")):
        if path.is_symlink():
            report.errors.append(f"Symlinks are not portable or safe to package: {path.relative_to(skill_dir)}")
        if path.is_file() and path.suffix == ".py" and "scripts" in path.parts:
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as exc:
                report.errors.append(f"Python syntax error in {path.relative_to(skill_dir)}: {exc.msg}")

    return report


def validate_skill(skill_dir: Path, strict: bool = False) -> list[str]:
    """Backward-compatible helper used by package_skill.py."""

    return validate_skill_report(skill_dir, strict=strict).errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a portable Agent Skill directory.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat product-specific or unknown frontmatter fields as errors",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] Not a directory: {skill_dir}")
        return 1

    report = validate_skill_report(skill_dir, strict=args.strict)
    for warning in report.warnings:
        print(f"[WARN] {warning}")
    for error in report.errors:
        print(f"[ERROR] {error}")

    if report.errors:
        return 1
    print("[OK] Skill is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
