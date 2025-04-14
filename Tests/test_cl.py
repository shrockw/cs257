import unittest
from ProductionCode.data import get_data


class TestData(unittest.TestCase):
    def test_data(self):
        '''
                Tests for the data.
                '''
        with open("loaded_data_test.csv", "r", encoding="utf-8") as f:
            data = f.readlines()
        self.assertEqual(get_data("test_data.csv"), data, "Should be the same")
