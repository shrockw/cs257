'''
Contains tests for the command line interface of the program.
'''

import unittest
import os
import ast
from ProductionCode.data import get_data, get_filepath


class TestData(unittest.TestCase):
    '''
    Extends the unittest.TestCase class to test the get_data function.
    '''

    def test_data(self):
        '''
        Tests for the data.
        '''

        expected_data_file_path = get_filepath("loaded_data_test.txt", "Tests")

        with open(expected_data_file_path, "r", encoding="utf-8") as f:
            expected_data = f.readlines()[0]

        self.assertEqual(get_data("test_data.csv", "Data"),
                         ast.literal_eval(expected_data), "Should be the same")


if __name__ == "__main__":
    unittest.main()
