#!/usr/bin/env python3
"""Generate a skills index in README.md from SKILL.md frontmatter."""

import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent
README = SKILLS_DIR / "README.md"
MARKER_START = "<!-- skills-index-start -->"
MARKER_END = "<!-- skills-index-end -->"


def parse_frontmatter(skill_md):
    text = skill_md.read_text()
    match = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
    if not match:
        return None

    fm = match.group(1)
    name = None
    description_lines = []
    in_description = False

    for line in fm.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
            in_description = False
        elif line.startswith("description:"):
            val = line.split(":", 1)[1].strip()
            if val.startswith(">"):
                in_description = True
            else:
                description_lines.append(val)
                in_description = False
        elif in_description:
            stripped = line.strip()
            if stripped and not re.match(r"^[a-z_-]+:", line):
                description_lines.append(stripped)
            else:
                in_description = False
        elif description_lines and not line.startswith(" ") and re.match(r"^[a-z_-]+:", line):
            in_description = False

    description = " ".join(description_lines)
    return {"name": name, "description": description}


def discover_skills():
    skills = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        if skill_md.parent.name.startswith(("_", ".")):
            continue
        info = parse_frontmatter(skill_md)
        if info and info["name"]:
            skills.append(info)
    return sorted(skills, key=lambda s: s["name"])


def build_index(skills):
    lines = [MARKER_START, "", "| Skill | Description |", "| --- | --- |"]
    for skill in skills:
        lines.append(f"| [{skill['name']}]({skill['name']}/) | {skill['description']} |")
    lines.append("")
    lines.append(MARKER_END)
    return "\n".join(lines)


def update_readme(index_block):
    if not README.exists():
        README.write_text(f"# Skills\n\n{index_block}\n")
        print(f"  created {README}")
        return

    content = README.read_text()

    if MARKER_START in content and MARKER_END in content:
        pattern = re.compile(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            re.DOTALL,
        )
        updated = pattern.sub(index_block, content)
    else:
        updated = content.rstrip() + "\n\n" + index_block + "\n"

    if updated != content:
        README.write_text(updated)
        print(f"  updated {README}")
    else:
        print(f"  ok {README} (no changes)")


def main():
    skills = discover_skills()
    if not skills:
        print("No skills found")
        return

    index_block = build_index(skills)
    update_readme(index_block)


if __name__ == "__main__":
    main()
