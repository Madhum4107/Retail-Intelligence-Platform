import unittest
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "retail_store_inventory.csv"
REQUIRED = {
    "Category", "Region", "Seasonality", "Units Sold",
    "Inventory Level", "Demand Forecast", "Price",
}


class RetailDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(DATA)

    def test_data_file_exists_and_has_rows(self):
        self.assertTrue(DATA.is_file())
        self.assertGreater(len(self.df), 0)
        self.assertGreaterEqual(self.df.shape[1], len(REQUIRED))

    def test_required_dashboard_columns(self):
        self.assertFalse(REQUIRED - set(self.df.columns))

    def test_numeric_columns_convert(self):
        for col in ["Units Sold", "Inventory Level", "Demand Forecast", "Price"]:
            values = pd.to_numeric(self.df[col], errors="coerce")
            self.assertEqual(values.notna().sum(), self.df[col].notna().sum(), col)

    def test_values_are_non_negative_when_present(self):
        for col in ["Units Sold", "Inventory Level", "Demand Forecast", "Price"]:
            values = pd.to_numeric(self.df[col], errors="coerce").dropna()
            self.assertTrue((values >= 0).all(), col)

    def test_category_and_region_have_values(self):
        for col in ["Category", "Region", "Seasonality"]:
            self.assertTrue(self.df[col].notna().any(), col)


if __name__ == "__main__":
    unittest.main()
