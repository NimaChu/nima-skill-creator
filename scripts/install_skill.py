#!/usr/bin/env python3
"""Install a portable Agent Skill into common agent product locations."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

from package_skill import iter_files
from validate_skill import extract_frontmatter, parse_top_level_frontmatter, validate_skill_report

TARGETS: dict[str, dict[str, str]] = {
    "agent": {"user": "~/.agents/skills", "project": ".agents/skills"},
    "codex": {"user": "${CODEX_HOME:-~/.codex}/skills", "project": ".agents/skills"},
    "claude-code": {"user": "~/.claude/skills", "project": ".claude/skills"},
    "opencode": {"user": "~/.config/opencode/skills", "project": ".opencode/skills"},
    "openclaw": {"user": "~/.openclaw/skills", "project": "skills"},
    "workbuddy": {"user": "~/.workbuddy/skills", "project": ".codebuddy/skills"},
}
ALIASES = {
    "claude": "claude-code",
    "codebuddy": "workbuddy",
    "open-code": "opencode",
    "open-claw": "openclaw",
}


def expand_shell_path(value: str) -> Path:
    if value.startswith("${CODEX_HOME:-") and value.endswith("}/skills"):
        fallback = value[len("${CODEX_HOME:-") : -len("}/skills")]
        base = os.environ.get("CODEX_HOME", fallback)
        return Path(base).expanduser() / "skills"
    return Path(os.path.expandvars(value)).expanduser()


def safe_extract(archive: Path, destination: Path) -> None:
    with ZipFile(archive) as zf:
        root = destination.resolve()
        for member in zf.infolist():
            candidate = (destination / member.filename).resolve()
            try:
                candidate.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"Unsafe archive member: {member.filename}") from exc
        zf.extractall(destination)


def resolve_skill_source(source: Path, temporary_root: Path | None = None) -> Path:
    source = source.expanduser().resolve()
    if source.is_dir():
        return source
    if source.is_file() and source.suffix == ".zip":
        if temporary_root is None:
            raise ValueError("A temporary extraction directory is required for archives.")
        safe_extract(source, temporary_root)
        if (temporary_root / "SKILL.md").exists():
            return temporary_root
        candidates = [path.parent for path in temporary_root.glob("*/SKILL.md")]
        if len(candidates) == 1:
            return candidates[0]
        raise ValueError("Archive must contain SKILL.md at its root or in one top-level directory.")
    raise ValueError(f"Source must be a skill directory or .zip archive: {source}")


def read_skill_name(skill_dir: Path) -> str:
    frontmatter_text, _ = extract_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    frontmatter, _, _ = parse_top_level_frontmatter(frontmatter_text)
    return frontmatter["name"]


def resolve_destination_root(
    target: str,
    scope: str,
    project_root: Path | None,
    destination: Path | None,
) -> Path:
    if destination is not None:
        return destination.expanduser().resolve()

    canonical_target = ALIASES.get(target, target)
    if canonical_target not in TARGETS:
        supported = ", ".join(sorted(TARGETS))
        raise ValueError(f"Unknown target '{target}'. Supported targets: {supported}")

    configured = TARGETS[canonical_target][scope]
    if scope == "user":
        return expand_shell_path(configured).resolve()

    base = (project_root or Path.cwd()).expanduser().resolve()
    return (base / configured).resolve()


def install_skill(
    source: Path,
    target: str,
    scope: str,
    project_root: Path | None = None,
    destination: Path | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> Path:
    source_is_archive = source.expanduser().suffix == ".zip"
    with tempfile.TemporaryDirectory(prefix="nima-skill-install-") as temp_dir:
        skill_dir = resolve_skill_source(source, Path(temp_dir))
        report = validate_skill_report(skill_dir, require_directory_match=not source_is_archive)
        if report.errors:
            raise ValueError("Validation failed:\n- " + "\n- ".join(report.errors))

        skill_name = read_skill_name(skill_dir)
        destination_root = resolve_destination_root(target, scope, project_root, destination)
        destination_dir = destination_root / skill_name

        if destination_dir.exists() and not force:
            raise FileExistsError(f"Destination already exists: {destination_dir}. Use --force to replace it.")
        if dry_run:
            return destination_dir

        destination_root.mkdir(parents=True, exist_ok=True)
        if destination_dir.exists():
            shutil.rmtree(destination_dir)
        destination_dir.mkdir(parents=True)
        for path in iter_files(skill_dir):
            relative = path.relative_to(skill_dir)
            target_path = destination_dir / relative
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target_path)
        return destination_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Install an Agent Skill for a supported agent product.")
    parser.add_argument("source", help="Skill directory or .skill.zip archive")
    parser.add_argument("--target", required=True, help="agent, codex, claude-code, opencode, openclaw, or workbuddy")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-root", help="Project root for project-scoped installation")
    parser.add_argument("--destination", help="Explicit destination root; overrides target defaults")
    parser.add_argument("--force", action="store_true", help="Replace an existing installed skill")
    parser.add_argument("--dry-run", action="store_true", help="Print the destination without copying files")
    args = parser.parse_args()

    try:
        destination = install_skill(
            source=Path(args.source),
            target=args.target,
            scope=args.scope,
            project_root=Path(args.project_root) if args.project_root else None,
            destination=Path(args.destination) if args.destination else None,
            force=args.force,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    action = "Would install to" if args.dry_run else "Installed to"
    print(f"[OK] {action} {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
