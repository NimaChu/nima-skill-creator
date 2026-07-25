#!/usr/bin/env python3
"""Create a clean, deterministic archive from a validated Agent Skill directory."""

from __future__ import annotations

import argparse
import stat
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from validate_skill import validate_skill_report

REPOSITORY_ONLY_ROOT_FILES = {
    ".gitignore",
    ".gitattributes",
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
}
REPOSITORY_ONLY_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    ".pytest_cache",
    "__pycache__",
    "docs",
    "tests",
    "dist",
    "build",
}
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def should_package(skill_dir: Path, path: Path) -> bool:
    relative = path.relative_to(skill_dir)
    if relative.parts[0] in REPOSITORY_ONLY_DIRS:
        return False
    if len(relative.parts) == 1 and relative.name in REPOSITORY_ONLY_ROOT_FILES:
        return False
    if path.name in IGNORED_NAMES:
        return False
    if path.suffix in {".pyc", ".pyo"}:
        return False
    if path.name.endswith((".skill", ".skill.zip")):
        return False
    return True


def iter_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed: {path.relative_to(skill_dir)}")
        if path.is_file() and should_package(skill_dir, path):
            yield path


def _zip_info(path: Path, arcname: str) -> ZipInfo:
    info = ZipInfo(arcname, ARCHIVE_TIMESTAMP)
    info.compress_type = ZIP_DEFLATED
    mode = path.stat().st_mode
    permissions = 0o755 if mode & stat.S_IXUSR else 0o644
    info.external_attr = permissions << 16
    return info


def package_skill(skill_dir: Path, output_dir: Path | None) -> Path:
    skill_dir = skill_dir.expanduser().resolve()
    report = validate_skill_report(skill_dir)
    if report.errors:
        raise ValueError("Validation failed:\n- " + "\n- ".join(report.errors))

    target_dir = (output_dir or skill_dir.parent).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    archive_path = target_dir / f"{skill_dir.name}.skill.zip"

    with ZipFile(archive_path, "w") as zf:
        for path in iter_files(skill_dir):
            arcname = path.relative_to(skill_dir).as_posix()
            zf.writestr(_zip_info(path, arcname), path.read_bytes())
    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Package a validated Agent Skill without repository-only files."
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("output_dir", nargs="?", help="Optional output directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] Not a directory: {skill_dir}")
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    try:
        archive = package_skill(skill_dir, output_dir)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"[OK] Created archive at {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
