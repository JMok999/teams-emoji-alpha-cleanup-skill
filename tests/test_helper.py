#!/usr/bin/env python3
"""Regression checks for scripts/clean_teams_emoji.py.

Run with:
    python tests/test_helper.py
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "scripts" / "clean_teams_emoji.py"
FIXTURE_PATH = ROOT / "tests" / "generate_fixtures.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


HELPER = load_module("teams_emoji_helper", HELPER_PATH)
FIXTURES = load_module("teams_emoji_fixtures", FIXTURE_PATH)


class TeamsEmojiHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tempdir = tempfile.TemporaryDirectory(prefix="teams-emoji-tests-")
        cls.workdir = Path(cls.tempdir.name)
        cls.fixtures = cls.workdir / "fixtures"
        FIXTURES.create_fixtures(cls.fixtures)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def _run_helper(self, fixture_name: str) -> Path:
        output = self.workdir / f"{Path(fixture_name).stem}_teams_emoji_256.webp"
        argv = [
            "clean_teams_emoji.py",
            str(self.fixtures / fixture_name),
            str(output),
        ]
        with patch.object(sys, "argv", argv):
            HELPER.main()
        self.assertTrue(output.is_file(), "The helper did not create an output file.")
        return output

    def _assert_teams_asset(self, output: Path) -> Image.Image:
        with Image.open(output) as encoded:
            self.assertEqual(encoded.format, "WEBP")
            self.assertIn("A", encoded.getbands(), "Encoded WebP has no alpha channel.")
            image = encoded.convert("RGBA")

        self.assertEqual(image.size, (256, 256))
        alpha = image.getchannel("A")
        self.assertIsNotNone(alpha.getbbox(), "Output has no visible subject.")

        for x in range(256):
            self.assertEqual(alpha.getpixel((x, 0)), 0)
            self.assertEqual(alpha.getpixel((x, 255)), 0)
        for y in range(256):
            self.assertEqual(alpha.getpixel((0, y)), 0)
            self.assertEqual(alpha.getpixel((255, y)), 0)

        preview_dir = output.parent / f"{output.stem}_previews"
        for name in ("white.png", "teams_light.png", "dark.png", "black.png"):
            self.assertTrue((preview_dir / name).is_file(), f"Missing preview: {name}")

        return image

    def test_white_background_preserves_internal_white_detail(self) -> None:
        output = self._run_helper("01-white-background-internal-white.png")
        image = self._assert_teams_asset(output)
        opaque_white_pixels = sum(
            1
            for r, g, b, a in image.getdata()
            if a > 230 and r > 240 and g > 240 and b > 240
        )
        self.assertGreater(
            opaque_white_pixels,
            20,
            "Expected enclosed white detail to remain after edge-connected cleanup.",
        )

    def test_existing_alpha_source_remains_valid(self) -> None:
        output = self._run_helper("02-existing-alpha.png")
        self._assert_teams_asset(output)

    def test_animated_gif_uses_a_static_first_frame(self) -> None:
        output = self._run_helper("07-animated-first-frame.gif")
        self._assert_teams_asset(output)

    def test_rejects_non_webp_output_path(self) -> None:
        argv = [
            "clean_teams_emoji.py",
            str(self.fixtures / "01-white-background-internal-white.png"),
            str(self.workdir / "wrong-extension.png"),
        ]
        with patch.object(sys, "argv", argv):
            with self.assertRaises(ValueError):
                HELPER.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
