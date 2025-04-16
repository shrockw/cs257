import unittest
import os
from ProductionCode.data import get_data


class TestData(unittest.TestCase):
    def test_data(self):
        '''
        Tests for the data.
        '''

        data_folder = os.path.join(os.path.dirname(__file__), '')
        file_path = os.path.join(data_folder, "loaded_data_test.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            data = f.readlines()
        self.assertEqual(get_data("test_data.csv"), data, "Should be the same")

if __name__ == "__main__":
    unittest.main()