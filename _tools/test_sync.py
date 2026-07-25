import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sync


class MainTests(unittest.TestCase):
    def test_invalid_toml_fails_without_traceback(self):
        error = sync.tomllib.TOMLDecodeError(
            "Unescaped '\\' in a string", 'path = "C:\\skills"', 10
        )
        stderr = io.StringIO()

        with mock.patch.object(sync, "load_config", side_effect=error):
            with contextlib.redirect_stderr(stderr):
                exit_code = sync.main()

        message = stderr.getvalue()
        self.assertEqual(exit_code, 2)
        self.assertIn("Invalid TOML in", message)
        self.assertIn("line 1, column", message)
        self.assertIn("escape backslashes", message)
        self.assertNotIn("Traceback", message)

    def test_load_config_accepts_literal_windows_path_in_unused_section(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.toml"
            config_path.write_text(
                f"""skills_dir = '{root}'
                [targets]
                test = '{root / "target"}'
                [notes]
                windows = 'C:\\Users\\example\\.agents\\skills'
                """
            )

            skills_dir, targets = sync.load_config(config_path)

        self.assertEqual(skills_dir, root.resolve())
        self.assertEqual(targets, [root / "target"])


if __name__ == "__main__":
    unittest.main()
