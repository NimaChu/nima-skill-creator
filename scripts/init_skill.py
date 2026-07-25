#!/usr/bin/env python3
"""Initialize a portable Agent Skill with optional product adapters."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from generate_openai_yaml import write_openai_yaml

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}
ALLOWED_ADAPTERS = {"openai"}

SKILL_BODY_TEMPLATE = """# {skill_title}

Use this skill when the request matches the capability and trigger scenarios in the description.

## Workflow

1. Confirm the concrete input, desired output, and constraints.
2. Load only the supporting references needed for the current task.
3. Run bundled scripts when deterministic execution is safer than rewriting logic.
4. Validate the result against the requested output and any bundled checklist.

## Instructions

Replace this section with the real, imperative workflow for the skill.

## Supporting resources

- `references/` contains detailed guidance that should load on demand.
- `scripts/` contains deterministic automation.
- `assets/` contains templates and static resources used in outputs.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""Example helper for {skill_name}. Replace or delete this file."""


def main() -> None:
    print("Example helper for {skill_name}")


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Notes

Replace this file with focused domain guidance that should only load on demand.
"""

EXAMPLE_ASSET = "Replace this placeholder with a real template or static resource.\n"


def normalize_skill_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


def title_case_skill_name(skill_name: str) -> str:
    return " ".join(part.capitalize() for part in skill_name.split("-") if part)


def parse_csv_values(raw_value: str, allowed: set[str], kind: str) -> list[str]:
    if not raw_value:
        return []
    result: list[str] = []
    for item in raw_value.split(","):
        item = item.strip()
        if not item or item in result:
            continue
        if item not in allowed:
            choices = ", ".join(sorted(allowed))
            raise ValueError(f"Unknown {kind} '{item}'. Allowed values: {choices}")
        result.append(item)
    return result


def parse_metadata(items: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid metadata '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError("Metadata keys and values must not be empty.")
        metadata[key] = value
    return metadata


def yaml_scalar(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9._/+ -]+", value) and not value.startswith(("-", "?", ":")):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_skill_md(
    skill_name: str,
    description: str,
    license_name: str | None,
    compatibility: str | None,
    metadata: dict[str, str],
) -> str:
    lines = ["---", f"name: {skill_name}", f"description: {yaml_scalar(description)}"]
    if license_name:
        lines.append(f"license: {yaml_scalar(license_name)}")
    if compatibility:
        lines.append(f"compatibility: {yaml_scalar(compatibility)}")
    if metadata:
        lines.append("metadata:")
        for key, value in metadata.items():
            lines.append(f"  {key}: {yaml_scalar(value)}")
    lines.extend(["---", "", SKILL_BODY_TEMPLATE.format(skill_title=title_case_skill_name(skill_name))])
    return "\n".join(lines).rstrip() + "\n"


def write_examples(skill_dir: Path, skill_name: str, resources: list[str]) -> None:
    if "scripts" in resources:
        path = skill_dir / "scripts" / "example.py"
        path.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8")
        path.chmod(0o755)
    if "references" in resources:
        (skill_dir / "references" / "reference.md").write_text(EXAMPLE_REFERENCE, encoding="utf-8")
    if "assets" in resources:
        (skill_dir / "assets" / "placeholder.txt").write_text(EXAMPLE_ASSET, encoding="utf-8")


def init_skill(
    skill_name: str,
    output_dir: Path,
    resources: list[str],
    include_examples: bool,
    adapters: list[str],
    interface_overrides: list[str],
    description: str,
    license_name: str | None,
    compatibility: str | None,
    metadata: dict[str, str],
) -> Path:
    normalized = normalize_skill_name(skill_name)
    if not normalized:
        raise ValueError("Skill name becomes empty after normalization.")
    if len(normalized) > MAX_SKILL_NAME_LENGTH:
        raise ValueError(
            f"Skill name is too long ({len(normalized)}). Maximum is {MAX_SKILL_NAME_LENGTH}."
        )

    skill_dir = output_dir.expanduser().resolve() / normalized
    if skill_dir.exists():
        raise FileExistsError(f"Skill directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        render_skill_md(
            normalized,
            description,
            license_name,
            compatibility,
            metadata,
        ),
        encoding="utf-8",
    )

    for resource in resources:
        (skill_dir / resource).mkdir()
    if include_examples:
        write_examples(skill_dir, normalized, resources)

    if interface_overrides and "openai" not in adapters:
        adapters.append("openai")
    if "openai" in adapters:
        write_openai_yaml(skill_dir, normalized, interface_overrides)

    return skill_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a portable Agent Skill directory.")
    parser.add_argument("skill_name", help="Skill name, preferably lowercase hyphen-case")
    parser.add_argument("--path", required=True, help="Parent directory for the skill")
    parser.add_argument(
        "--description",
        default="Explain what this skill does and when to use it. Include concrete trigger scenarios.",
    )
    parser.add_argument("--license", dest="license_name", help="Optional SPDX license identifier or file reference")
    parser.add_argument("--compatibility", help="Optional runtime or environment requirements")
    parser.add_argument("--metadata", action="append", default=[], help="Metadata entry in key=value format")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated resource directories: scripts,references,assets",
    )
    parser.add_argument("--examples", action="store_true", help="Create example files in selected resources")
    parser.add_argument(
        "--adapter",
        default="",
        help="Comma-separated optional product adapters. Currently supported: openai",
    )
    parser.add_argument("--interface", action="append", default=[], help="OpenAI adapter override in key=value format")
    args = parser.parse_args()

    try:
        resources = parse_csv_values(args.resources, ALLOWED_RESOURCES, "resource")
        adapters = parse_csv_values(args.adapter, ALLOWED_ADAPTERS, "adapter")
        metadata = parse_metadata(args.metadata)
        skill_dir = init_skill(
            skill_name=args.skill_name,
            output_dir=Path(args.path),
            resources=resources,
            include_examples=args.examples,
            adapters=adapters,
            interface_overrides=args.interface,
            description=args.description,
            license_name=args.license_name,
            compatibility=args.compatibility,
            metadata=metadata,
        )
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"[OK] Created skill at {skill_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
