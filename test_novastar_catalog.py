import unittest

from novastar_catalog import (
    calculate_panel_pixels,
    get_required_receiving_cards,
    get_recommended_controller,
    novastar_products,
)


class NovastarCatalogTests(unittest.TestCase):
    def test_calculate_panel_pixels(self):
        self.assertEqual(calculate_panel_pixels(960, 640, 2.5), (384, 256))

    def test_calculate_panel_pixels_rejects_zero_values(self):
        with self.assertRaises(ValueError):
            calculate_panel_pixels(960, 640, 0)

    def test_required_receiving_cards(self):
        result = get_required_receiving_cards(3840, 2160, 384, 256)
        self.assertEqual(result["cards_per_row"], 2)
        self.assertEqual(result["cards_per_col"], 2)
        self.assertEqual(result["total_cards"], 4)

    def test_required_receiving_cards_rejects_invalid_resolution(self):
        with self.assertRaises(ValueError):
            get_required_receiving_cards(0, 2160, 384, 256)

    def test_recommended_controller_rejects_invalid_resolution(self):
        with self.assertRaises(ValueError):
            get_recommended_controller(3840, 0)

    def test_recommends_available_controller_for_4k(self):
        models = {item["model"] for item in get_recommended_controller(3840, 2160)}
        self.assertIn("MCTRL4K", models)

    def test_catalog_contains_only_mctrl_series(self):
        self.assertTrue(novastar_products)
        self.assertTrue(all(item["model"].startswith("MCTRL") for item in novastar_products))

    def test_catalog_recommends_no_controller_above_loading_capacity(self):
        self.assertEqual(get_recommended_controller(7680, 7680), [])


if __name__ == "__main__":
    unittest.main()
