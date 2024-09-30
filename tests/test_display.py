# tests/test_display.py

import unittest
import pandas as pd
import os

class TestDisplay(unittest.TestCase):
    def test_excel_loading(self):
        excel_path = 'backend_data/data.xlsx'
        if not os.path.exists(excel_path):
            self.skipTest("Excel file not found.")

        try:
            df = pd.read_excel(excel_path)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertFalse(df.empty)
        except Exception as e:
            self.fail(f"Loading Excel failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
