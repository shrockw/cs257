'''
Contains tests for the command line interface of the program.
'''

import unittest
from unittest.mock import MagicMock, patch
import sys
from io import StringIO
import random
from ProductionCode.datasource import DataSource
from cl import main


class TestCommandLine(unittest.TestCase):
    '''
    Tests the command line interface.
    '''
    def setUp(self):
        '''
        Sets up the test environment by mocking the get_data function.
        '''
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        

class TestMainFunction(unittest.TestCase):
    '''
    Tests the main interface.
    '''
    def setUp(self):
        '''
        Sets up the test environment by mocking the get_data function.
        '''
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_main_random(self, mock_connect):
        '''Tests the main function for getting random recipes'''
        mock_connect.return_value = self.mock_conn

        # Set return value of fetchall on the mock cursor
        self.mock_cursor.fetchall.return_value = [(
            11286,
            'Chocolate and Peppermint Candy Ice Cream Sandwiches',
            'Stir together ice cream...',
            "['1 pint superpremium vanilla ice cream...']"
        )]

        sys.argv = ['cl.py', '--random', '1']
        sys.stdout = StringIO()
    
        main()

        output = sys.stdout.getvalue().strip()
        self.assertIn('Chocolate and Peppermint Candy Ice Cream Sandwiches', output)

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_command_line_search(self, mock_connect):
        '''
        Tests the command line interface.
        '''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [(13401, 'Thai-Style Chicken and Rice Soup', 'Combine stock, water, curry paste, garlic, ginger, coriander seeds, and whole cilantro leaves in a 3- to 4-quart saucepan, then simmer, uncovered, until ginger is softened, about 15 minutes. Pour through a paper-towel-lined sieve into a 5- to 6-quart heavy pot and discard solids. Stir rice into soup and simmer, uncovered, stirring occasionally, until tender, about 15 minutes.\nAdd chicken or shrimp and poach at a bare simmer, uncovered, until just cooked through, about 3 minutes. Stir in coconut milk, snow peas, and fish sauce and simmer, uncovered, until peas are crisp-tender, about 2 minutes. Remove from heat and stir in lime juice, salt, and chopped cilantro.\n*Available at Asian markets, some specialty foods shops, and some supermarkets.', "['8 cups chicken stock or low-sodium chicken broth (64 fl oz)', '4 cups water', '1 tablespoon Thai green curry paste*', '4 garlic cloves, coarsely chopped', '1 (2-inch) piece peeled fresh ginger, coarsely chopped', '1 teaspoon coriander seeds, crushed', '2 cups loosely packed whole fresh cilantro leaves plus 1/2 cup chopped (from 2 large bunches)', '1 cup jasmine rice', '3/4 lb boneless skinless chicken breast, thinly sliced crosswise, then slices cut lengthwise into thin strips, or 3/4 lb medium shrimp in shell (31 to 35 per lb), peeled and deveined', '1 (13- to 14-oz) can unsweetened coconut milk, stirred well', '1/4 lb snow peas, trimmed and cut diagonally into 1/4-inch strips', '2 tablespoons Asian fish sauce', '2 tablespoons fresh lime juice', '1 1/2 teaspoons salt, or to taste', 'Accompaniment: lime wedges']")]

        # Test the command line interface with the --include option
        sys.argv = ['cl.py', '--search',
                    '--include_ingredients', 'chicken, rice']
        sys.stdout = StringIO()

        main()

        output = sys.stdout.getvalue().strip()
        self.assertIn('Thai-Style Chicken and Rice Soup', output, "Should be the same")

        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [(13483, 'White Chicken Chili', 'In a large kettle soak beans in cold water to cover by 2 inches overnight. Drain beans in a colander and return to kettle with cold water to cover by 2 inches. Cook beans at a bare simmer until tender, about 1 hour, and drain in colander.\nIn a skillet cook onion in 2 tablespoons butter over moderate heat until softened.\nIn a 6- to 8-quart heavy kettle melt remaining 6 tablespoons butter over moderately low heat and whisk in flour. Cook roux, whisking constantly, 3 minutes. Stir in onion and gradually add broth and half-and-half, whisking constantly. Bring mixture to a boil and simmer, stirring occasionally, 5 minutes, or until thickened. Stir in Tabasco, chili powder, cumin, salt, and white pepper. Add beans, chilies, chicken, and Monterey Jack and cook mixture over moderately low heat, stirring, 20 minutes. Stir sour cream into chili.\nGarnish chili with coriander and serve with salsa.', "['1/2 pound dried navy beans, picked over', '1 large onion, chopped', '1 stick (1/2 cup) unsalted butter', '1/4 cup all-purpose flour', '3/4 cup chicken broth', '2 cups half-and-half', '1 teaspoon Tabasco, or to taste', '1 1/2 teaspoons chili powder', '1 teaspoon ground cumin', '1/2 teaspoon salt, or to taste', '1/2 teaspoon white pepper, or to taste', 'two 4-ounce cans whole mild green chilies, drained and chopped', '5 boneless skinless chicken breast halves (about 2 pounds), cooked and cut into 1/2-inch pieces', '1 1/2 cups grated Monterey Jack (about 6 ounces)', '1/2 cup sour cream', 'Garnish: fresh coriander sprigs', 'Accompaniment: tomato salsa']")]

        # Test the command line interface with both --incluce and --omit option
        sys.argv = ['cl.py', '--search', '--include_ingredients',
                    'chicken', '--omit_ingredients', 'kale']
        sys.stdout = StringIO()

        main()

        output = sys.stdout.getvalue().strip()
        self.assertIn('White Chicken Chili', output, "Should be the same")

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_command_line_omit(self, mock_connect):
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [(13499, 'Spanakopita', 'Melt 1 tablespoon butter in a 12-inch heavy skillet over moderate heat, then cook spinach, stirring, until wilted and tender, about 4 minutes. Remove from heat and cool, about 10 minutes. Squeeze handfuls of spinach to remove as much liquid as possible, then coarsely chop. Transfer to a bowl and stir in feta, nutmeg, 1/2 teaspoon salt, and 1/2 teaspoon pepper.\nPreheat oven to 375°F.\nMelt remaining 1 stick butter in a small saucepan, then cool.\nCover phyllo stack with 2 overlapping sheets of plastic wrap and then a dampened kitchen towel.\nTake 1 phyllo sheet from stack and arrange on a work surface with a long side nearest you (keeping remaining sheets covered) and brush with some butter. Top with another phyllo sheet and brush with more butter. Cut buttered phyllo stack crosswise into 6 (roughly 12- by 2 3/4-inch) strips.\nPut a heaping teaspoon of filling near 1 corner of a strip on end nearest you, then fold corner of phyllo over to enclose filling and form a triangle. Continue folding strip (like a flag), maintaining triangle shape. Put triangle, seam side down, on a large baking sheet and brush top with butter. Make more triangles in same manner, using all of phyllo.\nBake triangles in middle of oven until golden brown, 20 to 25 minutes, then transfer to a rack to cool slightly.', "['1 stick (1/2 cup) plus 1 tablespoon unsalted butter', '1 lb baby spinach', '1/2 lb feta, crumbled (scant 2 cups)', '1/2 teaspoon freshly grated nutmeg', '10 (17- by 12-inch) phyllo sheets', 'thawed if frozen']")]

        # Test the command line interface with --omit option
        sys.argv = ['cl.py', '--search', '--omit_ingredients', 'chicken']
        sys.stdout = StringIO()

        main()

        output = sys.stdout.getvalue().strip()
        self.assertIn('Spanakopita', output, "Should be the same")

    def test_command_line_help(self):
        '''
        Tests the command line interface.
        '''

        # Test the command line interface with the --help option
        sys.argv = ['cl.py', '--help']
        sys.stdout = StringIO()

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 0, "Exit code should be 0")

        expected_output = "usage: cl.py [-h] (-s | -r n)"
        expected_output = expected_output.strip()

        output = sys.stdout.getvalue().strip()
        self.assertIn(expected_output, output, "Should be the same")


if __name__ == "__main__":
    unittest.main()
