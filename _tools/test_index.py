import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import index


class ParseFrontmatterTests(unittest.TestCase):
    def test_parses_folded_description(self):
        with tempfile.TemporaryDirectory() as directory:
            skill_md = Path(directory) / "SKILL.md"
            skill_md.write_text(
                """---
name: example-skill
description: >-
  First line of the description.
  Second line.
when_to_use: example
---
Instructions
"""
            )

            result = index.parse_frontmatter(skill_md)

        self.assertEqual(
            result,
            {
                "name": "example-skill",
                "description": "First line of the description. Second line.",
            },
        )

    def test_returns_none_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            skill_md = Path(directory) / "SKILL.md"
            skill_md.write_text("# Example\n")

            self.assertIsNone(index.parse_frontmatter(skill_md))


class IndexTests(unittest.TestCase):
    def test_discovers_named_skills_in_name_order(self):
        with tempfile.TemporaryDirectory() as directory:
            skills_dir = Path(directory)
            for folder, name in (
                ("z-folder", "alpha"),
                ("a-folder", "zulu"),
                ("_tools", "ignored"),
            ):
                skill_dir = skills_dir / folder
                skill_dir.mkdir()
                (skill_dir / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: {name} description\n---\n"
                )

            with mock.patch.object(index, "SKILLS_DIR", skills_dir):
                skills = index.discover_skills()

        self.assertEqual([skill["name"] for skill in skills], ["alpha", "zulu"])

    def test_builds_marked_markdown_table(self):
        result = index.build_index(
            [{"name": "example", "description": "Example description"}]
        )

        self.assertEqual(
            result,
            """<!-- skills-index-start -->

| Skill | Description |
| --- | --- |
| [example](example/) | Example description |

<!-- skills-index-end -->""",
        )

    def test_replaces_existing_index_and_preserves_surrounding_content(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(
                "# Skills\n\n"
                f"{index.MARKER_START}\nold index\n{index.MARKER_END}\n\n"
                "Footer\n"
            )
            new_block = index.build_index(
                [{"name": "new-skill", "description": "New description"}]
            )

            with mock.patch.object(index, "README", readme):
                with contextlib.redirect_stdout(io.StringIO()):
                    index.update_readme(new_block)

            result = readme.read_text()

        self.assertIn("# Skills", result)
        self.assertIn("[new-skill](new-skill/)", result)
        self.assertNotIn("old index", result)
        self.assertTrue(result.endswith("Footer\n"))

    def test_creates_missing_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            block = index.build_index([])

            with mock.patch.object(index, "README", readme):
                with contextlib.redirect_stdout(io.StringIO()):
                    index.update_readme(block)

            result = readme.read_text()

        self.assertEqual(result, f"# Skills\n\n{block}\n")


if __name__ == "__main__":
    unittest.main()
