import json
import tempfile
import unittest
from pathlib import Path

from panel_archive import (
    calculate_total_max_absorption,
    load_panel_archive,
    save_panel_profile,
)


class PanelArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.archive_path = Path(self.temp_dir.name) / "panels.json"
        self.archive_path.write_text("[]\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_saves_and_reloads_a_panel_profile(self):
        profile = {
            "name": "Indoor 2.5",
            "manufacturer": "MRLED",
            "project": "Bicocca",
            "width_mm": 960,
            "height_mm": 640,
            "pixel_pitch_mm": 2.5,
            "max_absorption_w": 500,
        }

        saved = save_panel_profile(profile, self.archive_path)

        self.assertEqual(saved, [profile])
        self.assertEqual(load_panel_archive(self.archive_path), [profile])
        self.assertEqual(json.loads(self.archive_path.read_text(encoding="utf-8")), [profile])

    def test_rejects_duplicate_panel_profile(self):
        profile = {
            "name": "Indoor 2.5",
            "manufacturer": "MRLED",
            "project": "Bicocca",
            "width_mm": 960,
            "height_mm": 640,
            "pixel_pitch_mm": 2.5,
            "max_absorption_w": 500,
        }
        save_panel_profile(profile, self.archive_path)

        with self.assertRaisesRegex(ValueError, "già presente"):
            save_panel_profile({**profile, "name": " indoor 2.5 "}, self.archive_path)

    def test_rejects_non_positive_maximum_absorption(self):
        profile = {
            "name": "Indoor 2.5",
            "manufacturer": "MRLED",
            "project": "Bicocca",
            "width_mm": 960,
            "height_mm": 640,
            "pixel_pitch_mm": 2.5,
            "max_absorption_w": 0,
        }

        with self.assertRaisesRegex(ValueError, "maggiore di zero"):
            save_panel_profile(profile, self.archive_path)

    def test_calculates_total_maximum_absorption(self):
        self.assertEqual(calculate_total_max_absorption(12, 500), 6000)

    def test_rejects_invalid_absorption_calculation(self):
        with self.assertRaises(ValueError):
            calculate_total_max_absorption(12, 0)


if __name__ == "__main__":
    unittest.main()
