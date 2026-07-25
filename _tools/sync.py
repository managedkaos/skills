#!/usr/bin/env python3
"""Sync individual skills into AI tool directories via per-skill symlinks."""

import os
import sys
import tomllib
from pathlib import Path


def load_config(config_path=None):
    config_path = config_path or Path(__file__).parent / "config.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    skills_dir = Path(os.environ.get("SKILLS_DIR", config["skills_dir"])).expanduser().resolve()

    if env_targets := os.environ.get("SKILLS_TARGETS"):
        targets = [Path(p).expanduser() for p in env_targets.split(":")]
    else:
        targets = [Path(p).expanduser() for p in config["targets"].values()]

    return skills_dir, targets


def discover_skills(skills_dir):
    skills = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        name = skill_md.parent.name
        if not name.startswith(("_", ".")):
            skills.append(name)
    return skills


def sync_target(skills_dir, target, skills):
    target.mkdir(parents=True, exist_ok=True)

    for name in skills:
        link = target / name
        source = skills_dir / name

        if link.is_symlink():
            current = Path(os.readlink(link))
            if current == source:
                print(f"  ok  {link}")
            else:
                link.unlink()
                link.symlink_to(source)
                print(f"  fix {link} (was {current})")
        elif link.exists():
            print(f" skip {link} (not a symlink, won't overwrite)")
        else:
            link.symlink_to(source)
            print(f"  add {link}")

    for entry in sorted(target.iterdir()):
        if not entry.is_symlink():
            continue
        resolved = Path(os.readlink(entry))
        if str(resolved).startswith(str(skills_dir)):
            if entry.name not in skills:
                entry.unlink()
                print(f"  rm  {entry} (skill removed)")


def main():
    config_path = Path(__file__).parent / "config.toml"
    try:
        skills_dir, targets = load_config(config_path)
    except tomllib.TOMLDecodeError as error:
        print(f"Invalid TOML in {config_path}: {error}", file=sys.stderr)
        if "Unescaped '\\'" in str(error):
            print(
                "Hint: escape backslashes as '\\\\' or use a TOML literal "
                "string enclosed in single quotes.",
                file=sys.stderr,
            )
        return 2

    if not skills_dir.is_dir():
        print(f"Skills directory not found: {skills_dir}")
        return 1

    skills = discover_skills(skills_dir)
    if not skills:
        print(f"No skills found in {skills_dir}")
        return 1

    for target in targets:
        sync_target(skills_dir, target, skills)

    return 0


if __name__ == "__main__":
    sys.exit(main())
