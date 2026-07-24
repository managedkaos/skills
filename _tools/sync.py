#!/usr/bin/env python3
"""Sync skills directory into AI tool locations via whole-directory symlinks."""

import os
import shutil
import tomllib
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent / "config.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    skills_dir = Path(os.environ.get("SKILLS_DIR", config["skills_dir"])).expanduser().resolve()

    if env_targets := os.environ.get("SKILLS_TARGETS"):
        targets = [Path(p).expanduser() for p in env_targets.split(":")]
    else:
        targets = [Path(p).expanduser() for p in config["targets"].values()]

    return skills_dir, targets


def is_safe_to_replace(target, skills_dir):
    """Check if a real directory is safe to replace (empty or only contains our symlinks)."""
    for entry in target.iterdir():
        if entry.is_symlink():
            resolved = Path(os.readlink(entry))
            if not str(resolved).startswith(str(skills_dir)):
                return False
        else:
            return False
    return True


def sync_target(skills_dir, target):
    if target.is_symlink():
        current = target.resolve()
        if current == skills_dir:
            print(f"  ok  {target} → {skills_dir}")
        else:
            target.unlink()
            target.symlink_to(skills_dir)
            print(f"  fix {target} (was → {current})")
    elif target.is_dir():
        if is_safe_to_replace(target, skills_dir):
            shutil.rmtree(target)
            target.symlink_to(skills_dir)
            print(f"  fix {target} (replaced directory with symlink)")
        else:
            print(f" skip {target} (directory with non-managed content, won't overwrite)")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(skills_dir)
        print(f"  add {target} → {skills_dir}")


def main():
    skills_dir, targets = load_config()

    if not skills_dir.is_dir():
        print(f"Skills directory not found: {skills_dir}")
        return

    for target in targets:
        sync_target(skills_dir, target)


if __name__ == "__main__":
    main()
