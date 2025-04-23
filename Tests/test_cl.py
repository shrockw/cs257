'''
Contains tests for the command line interface of the program.
'''

import unittest
import unittest.mock
import sys
from io import StringIO
import random
from ProductionCode.data import get_data
from ProductionCode.recipe_search import find_recipes
from ProductionCode.random_recipe import get_random_recipes
from cl import search, random_cl, help_cl, main


class TestData(unittest.TestCase):
    '''
    Extends the unittest.TestCase class to test the get_data function.
    '''

    def test_data(self):
        '''
        Tests for the data.
        '''

        recipe = ['10', 'Hot Pimento Cheese Dip', 'Put the chipotle peppers and adobo sauce in '
        'a small food processor or blender and blend until the mixture turns into a smooth purée. '
        'Set aside. The chipotle purée can be made in advance, stored in an airtight container, '
        'and refrigerated for up to 2 months.\nOn a cutting board, sprinkle the garlic with a '
        'large pinch of salt and gather it into a small mound. Holding the blunt side of the knife '
        'with both hands, press and scrape the knife’s sharp end, holding it at a slight angle, '
        'across the garlic mound to flatten it. Repeat, dragging it across the garlic, until you '
        'have a smooth paste. Set aside.\nIn a small bowl, mix the cornstarch and 1½ tsp. of the '
        'evaporated milk into a slurry. Pour the rest of the evaporated milk into a medium '
        'saucepan and stir in the slurry. Bring to a boil over medium-high heat, whisking '
        'constantly. Turn the heat to low and add the Cheddar gradually by the handful, stirring '
        'until the Cheddar is melted and the mixture is smooth. Add the cream cheese and whisk '
        'until it melts. Stir in the mayonnaise, pimento peppers, 1½ tsp. of the chipotle purée, '
        'and the garlic paste. Season with salt. Transfer to a serving bowl or keep it warm '
        'in a slow cooker and serve immediately.\nTo reheat the sauce, microwave it, stirring '
        'every 30 seconds, until fully melted.', 
        ['1 (7 oz./200 g) can chipotle in adobo sauce', '½ garlic clove, minced', 'Kosher salt',
         '1½ tsp. cornstarch', '1 (5 fl oz./150 ml) can evaporated milk (about ½ cup plus 2 Tbsp)', 
         '8 oz. (230 g) sharp or extra-sharp Cheddar cheese, coarsely grated (about 2 cups)', 
         '2 oz. (55 g) cream cheese, roughly diced, at room temperature', '¼ cup (60 g) mayonnaise', 
         '1 (4 oz./115 g) jar diced pimento peppers, drained', '1½ tsp. Chipotle Pepper Purée']]
        self.assertIn(recipe, get_data(), "Should be the same")


class TestRandomRecipe(unittest.TestCase):
    '''
    Tests the random recipe function.
    '''

    def setUp(self):
        random.seed(931254)
        self.test_recipes = [
            ['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']],
            ['1', 'Title2', 'Instructions for Title2', ['Ingredient3', 'Ingredient4']],
            ['2', 'Title3', 'Instructions for Title3', ['Ingredient5', 'Ingredient6']],
            ['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']],
            ['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']],
            ['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']],
            ['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']],
            ['7', 'Title8', 'Instructions for Title8',
             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
            ['8', 'Title9', 'Instructions for Title9',
             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
            ['9', 'Title10', 'Instructions for Title10',
             ['Ingredient4', 'Ingredient8', 'Ingrediente']]
        ]

    def test_random_recipe(self):
        '''
        Tests the random recipe function.
        '''

        expected_recipes = [['9', 'Title10', 'Instructions for Title10', [
            'Ingredient4', 'Ingredient8', 'Ingrediente']]]
        self.assertEqual(get_random_recipes(self.test_recipes, 1),
                         expected_recipes, "Should be the same")

        expected_recipes = [['6', 'Title7', 'Instructions for Title7',
                             ['Ingredientd', 'Ingrediente']],
                            ['3', 'Title4', 'Instructions for Title4',
                             ['Ingredient7', 'Ingredient8']],
                            ['7', 'Title8', 'Instructions for Title8',
                             ['Ingredientf', 'Ingredientg', 'Ingredient3']]]

        self.assertEqual(get_random_recipes(self.test_recipes, 3),
                         expected_recipes, "Should be the same")

        expected_recipes = []
        self.assertEqual(get_random_recipes(self.test_recipes, 0),
                         expected_recipes, "Should be the same")

    def test_random_recipe_invalid(self):
        '''
        Tests the random recipe function with invalid input.
        '''

        with self.assertRaises(ValueError):
            get_random_recipes(self.test_recipes, -1)

        with self.assertRaises(ValueError):
            get_random_recipes(self.test_recipes, 100)


class TestRecipeSearch(unittest.TestCase):
    '''
    Tests the recipe search function.
    '''

    def setUp(self):
        self.test_recipes = [
            ['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']],
            ['1', 'Title2', 'Instructions for Title2', ['Ingredient3', 'Ingredient4']],
            ['2', 'Title3', 'Instructions for Title3', ['Ingredient5', 'Ingredient6']],
            ['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']],
            ['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']],
            ['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']],
            ['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']],
            ['7', 'Title8', 'Instructions for Title8',
             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
            ['8', 'Title9', 'Instructions for Title9',
             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
            ['9', 'Title10', 'Instructions for Title10',
             ['Ingredient4', 'Ingredient8', 'Ingrediente']]
        ]

    def test_recipe_search_wanted(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [['0', 'Title1', 'Instructions for Title1',
                             ['Ingredient1', 'Ingredient2']],
                            ['8', 'Title9', 'Instructions for Title9',
                             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']]]
        self.assertEqual(find_recipes(self.test_recipes, ["Ingredient1"], [
        ]), expected_recipes, "Should be the same")

        expected_recipes = []
        self.assertEqual(find_recipes(self.test_recipes, ["Ingredient1", "Ingredient3"], [
        ]), expected_recipes, "Should be the same")

        expected_recipes = [['0', 'Title1', 'Instructions for Title1',
                             ['Ingredient1', 'Ingredient2']],
                            ['1', 'Title2', 'Instructions for Title2',
                             ['Ingredient3', 'Ingredient4']],
                            ['2', 'Title3', 'Instructions for Title3',
                             ['Ingredient5', 'Ingredient6']],
                            ['3', 'Title4', 'Instructions for Title4',
                             ['Ingredient7', 'Ingredient8']],
                            ['4', 'Title5', 'Instructions for Title5',
                             ['Ingredient9', 'Ingredienta']],
                            ['5', 'Title6', 'Instructions for Title6',
                             ['Ingredientb', 'Ingredientc']],
                            ['6', 'Title7', 'Instructions for Title7',
                             ['Ingredientd', 'Ingrediente']],
                            ['7', 'Title8', 'Instructions for Title8',
                             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
                            ['8', 'Title9', 'Instructions for Title9',
                             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
                            ['9', 'Title10', 'Instructions for Title10',
                             ['Ingredient4', 'Ingredient8', 'Ingrediente']]]
        self.assertEqual(find_recipes(self.test_recipes, ["Ingredient"], [
        ]), expected_recipes, "Should be the same")

    def test_recipe_search_unwanted(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [['0', 'Title1', 'Instructions for Title1',
                             ['Ingredient1', 'Ingredient2']],
                            ['1', 'Title2', 'Instructions for Title2',
                             ['Ingredient3', 'Ingredient4']],
                            ['3', 'Title4', 'Instructions for Title4',
                             ['Ingredient7', 'Ingredient8']],
                            ['4', 'Title5', 'Instructions for Title5',
                             ['Ingredient9', 'Ingredienta']],
                            ['5', 'Title6', 'Instructions for Title6',
                             ['Ingredientb', 'Ingredientc']],
                            ['6', 'Title7', 'Instructions for Title7',
                             ['Ingredientd', 'Ingrediente']],
                            ['7', 'Title8', 'Instructions for Title8',
                             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
                            ['8', 'Title9', 'Instructions for Title9',
                             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
                            ['9', 'Title10', 'Instructions for Title10',
                             ['Ingredient4', 'Ingredient8', 'Ingrediente']]]
        
        self.assertEqual(find_recipes(self.test_recipes, [], [
                         "Ingredient5"]), expected_recipes, "Should be the same")

        expected_recipes = [['0', 'Title1', 'Instructions for Title1',
                             ['Ingredient1', 'Ingredient2']],
                            ['1', 'Title2', 'Instructions for Title2',
                             ['Ingredient3', 'Ingredient4']],
                            ['2', 'Title3', 'Instructions for Title3',
                             ['Ingredient5', 'Ingredient6']],
                            ['3', 'Title4', 'Instructions for Title4',
                             ['Ingredient7', 'Ingredient8']],
                            ['5', 'Title6', 'Instructions for Title6',
                             ['Ingredientb', 'Ingredientc']],
                            ['7', 'Title8', 'Instructions for Title8',
                             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
                            ['8', 'Title9', 'Instructions for Title9',
                             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']]]
        self.assertEqual(find_recipes(self.test_recipes, [], [
                         "Ingrediente", "Ingredient9"]), expected_recipes, "Should be the same")

        expected_recipes = []
        self.assertEqual(find_recipes(self.test_recipes, [], [
                         "Ingredient"]), expected_recipes, "Should be the same")

    def test_recipe_search_both(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [
            ['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']]]


        self.assertEqual(find_recipes(self.test_recipes, ["Ingredient1", "Ingredient2"], [
                         "Ingredient11"]), expected_recipes, "Should be the same")

        expected_recipes = [['0', 'Title1', 'Instructions for Title1',
                             ['Ingredient1', 'Ingredient2']],
                            ['1', 'Title2', 'Instructions for Title2',
                             ['Ingredient3', 'Ingredient4']],
                            ['2', 'Title3', 'Instructions for Title3',
                             ['Ingredient5', 'Ingredient6']],
                            ['3', 'Title4', 'Instructions for Title4',
                             ['Ingredient7', 'Ingredient8']],
                            ['4', 'Title5', 'Instructions for Title5',
                             ['Ingredient9', 'Ingredienta']],
                            ['5', 'Title6', 'Instructions for Title6',
                             ['Ingredientb', 'Ingredientc']],
                            ['6', 'Title7', 'Instructions for Title7',
                             ['Ingredientd', 'Ingrediente']],
                            ['7', 'Title8', 'Instructions for Title8',
                             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
                            ['8', 'Title9', 'Instructions for Title9',
                             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
                             ['9', 'Title10', 'Instructions for Title10',
                              ['Ingredient4', 'Ingredient8', 'Ingrediente']]]

        self.assertEqual(find_recipes(self.test_recipes, [], []),
                         expected_recipes, "Should be the same")

        expected_recipes = []
        self.assertEqual(find_recipes(self.test_recipes, ["Ingredient"], [
                         "Ingredient"]), expected_recipes, "Should be the same")

        expected_recipes = []
        self.assertEqual(find_recipes(self.test_recipes, ["Ingredient4"], [
                         "Ingredient4"]), expected_recipes, "Should be the same")


class TestCommandLine(unittest.TestCase):
    '''
    Tests the command line interface.
    '''
    def setUp(self):
        '''
        Sets up the test environment by mocking the get_data function.
        '''
        self.patcher = unittest.mock.patch('cl.get_data')
        self.mock_get_data = self.patcher.start()
        self.mock_get_data.return_value = [
            ['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']],
            ['1', 'Title2', 'Instructions for Title2', ['Ingredient3', 'Ingredient4']],
            ['2', 'Title3', 'Instructions for Title3', ['Ingredient5', 'Ingredient6']],
            ['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']],
            ['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']],
            ['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']],
            ['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']],
            ['7', 'Title8', 'Instructions for Title8',
             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
            ['8', 'Title9', 'Instructions for Title9',
             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
            ['9', 'Title10', 'Instructions for Title10',
             ['Ingredient4', 'Ingredient8', 'Ingrediente']]
        ]

    def tearDown(self):
        '''
        Stops the patcher after the test.
        '''
        self.patcher.stop()


    def test_command_line_random(self):
        '''Tests the command line interface for getting random recipes'''

        sys.argv = ['cl.py', '--random', '1']
        sys.stdout = StringIO()

        expected_recipe = "['1', 'Title2', 'Instructions for Title2', "\
            "['Ingredient3', 'Ingredient4']]"

        random.seed(32719)

        random_cl()

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipe, "Should be the same")

    def test_command_line_search(self):
        '''
        Tests the command line interface search function.
        '''

        # Test the command line interface with the --include option
        sys.argv = ['cl.py', '--search',
                    '--include_ingredients', 'Ingredient1, Ingredient2']
        sys.stdout = StringIO()

        search()

        expected_recipes = "['0', 'Title1', 'Instructions for Title1', " \
            "['Ingredient1', 'Ingredient2']]"

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipes, "Should be the same")

        # Test the command line interface with both --incluce and --omit option
        sys.argv = ['cl.py', '--search', '--include_ingredients',
                    'Ingredient1', '--omit_ingredients', 'Ingredient2']
        sys.stdout = StringIO()

        search()

        expected_recipes = "['8', 'Title9', 'Instructions for Title9', " \
            "['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']]"

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipes, "Should be the same")

        # Test the command line interface with --omit option
        sys.argv = ['cl.py', '--search', '--omit_ingredients', 'Ingredient1']
        sys.stdout = StringIO()

        search()

        expected_recipes = "['1', 'Title2', 'Instructions for Title2', "\
            "['Ingredient3', 'Ingredient4']]\n" \
            "['2', 'Title3', 'Instructions for Title3', ['Ingredient5', 'Ingredient6']]\n" \
            "['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']]\n" \
            "['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']]\n" \
            "['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']]\n" \
            "['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']]\n" \
            "['7', 'Title8', 'Instructions for Title8', "\
            "['Ingredientf', 'Ingredientg', 'Ingredient3']]\n" \
            "['9', 'Title10', 'Instructions for Title10', " \
            "['Ingredient4', 'Ingredient8', 'Ingrediente']]"
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipes, "Should be the same")

    def test_command_line_help(self):
        '''
        Tests the command line interface.
        '''

        # Test the command line interface with the --help option
        sys.argv = ['cl.py', '--help']
        sys.stdout = StringIO()

        help_cl()

        expected_output = "Usage: python cl.py --search --include_ingredients " \
            "<ingredients> --omit_ingredients <ingredients>\n""<ingredients> should be a " \
            "comma-separated list of ingredients enclosed in quotes.\n""or python cl.py " \
            "--random <number>\n""or python cl.py --help\n""--search or --s: Search for a " \
            "specific recipe.\n""--random or --r: Get a random recipe.\n""--help or --h: " \
            "Display this help message."

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_output, "Should be the same")

    def test_bad_cl_input(self):
        '''
        Tests the command line interface with bad input.
        '''

        sys.argv = ['cl.py']
        sys.stdout = StringIO()

        main()

        expected_output = "Usage: python cl.py --search --include_ingredients " \
            "<ingredients> --omit_ingredients <ingredients>\n<ingredients> should be " \
            "a comma-separated list of ingredients enclosed in quotes.\nor python cl.py " \
            "--random <number>\nor python cl.py --help\n--search or --s: Search for a " \
            "specific recipe.\n--random or --r: Get a random recipe.\n--help or --h: " \
            "Display help message."

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_output, "Should be the same")

        # Test the command line interface with invalid input
        sys.argv = ['cl.py', '--search', '--include_ingredients',
                    'Ingredient1', '--omit_ingredients', 'Ingredient2', 'extra_arg']
        sys.stdout = StringIO()

        main()

        expected_output = "Usage: python cl.py --search --include_ingredients <ingredients> " \
            "--omit_ingredients <ingredients>\n<ingredients> should be a comma-separated list of " \
            "ingredients enclosed in quotes.\nor python cl.py --random <number>\nor python cl.py " \
            "--help\n--search or --s: Search for a specific recipe.\n--random or --r: Get a " \
            "random recipe.\n--help or --h: Display help message."

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_output, "Should be the same")


class TestMainFunction(unittest.TestCase):
    '''
    Tests the main interface.
    '''
    def setUp(self):
        '''
        Sets up the test environment by mocking the get_data function.
        '''
        self.patcher = unittest.mock.patch('cl.get_data')
        self.mock_get_data = self.patcher.start()
        self.mock_get_data.return_value = [
            ['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']],
            ['1', 'Title2', 'Instructions for Title2', ['Ingredient3', 'Ingredient4']],
            ['2', 'Title3', 'Instructions for Title3', ['Ingredient5', 'Ingredient6']],
            ['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']],
            ['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']],
            ['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']],
            ['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']],
            ['7', 'Title8', 'Instructions for Title8',
             ['Ingredientf', 'Ingredientg', 'Ingredient3']],
            ['8', 'Title9', 'Instructions for Title9',
             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']],
            ['9', 'Title10', 'Instructions for Title10',
             ['Ingredient4', 'Ingredient8', 'Ingrediente']]
        ]

    def tearDown(self):
        '''
        Stops the patcher after the test.
        '''
        self.patcher.stop()

    def test_main_random(self):
        '''Tests the main function for getting random recipes'''

        sys.argv = ['cl.py', '--random', '1']
        sys.stdout = StringIO()

        expected_recipe = "Getting random recipe...\n['1', 'Title2', 'Instructions for Title2', " \
            "['Ingredient3', 'Ingredient4']]"

        random.seed(32719)

        main()

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipe, "Should be the same")

    def test_command_line_search(self):
        '''
        Tests the command line interface.
        '''

        # Test the command line interface with the --include option
        sys.argv = ['cl.py', '--search',
                    '--include_ingredients', 'Ingredient1, Ingredient2']
        sys.stdout = StringIO()

        main()

        expected_recipes = "Searching for recipes...\n['0', 'Title1', 'Instructions for Title1', " \
            "['Ingredient1', 'Ingredient2']]"

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipes, "Should be the same")

        # Test the command line interface with both --incluce and --omit option
        sys.argv = ['cl.py', '--search', '--include_ingredients',
                    'Ingredient1', '--omit_ingredients', 'Ingredient2']
        sys.stdout = StringIO()

        main()

        expected_recipes = "Searching for recipes...\n['8', 'Title9', 'Instructions for Title9', " \
            "['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']]"

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipes, "Should be the same")

        # Test the command line interface with --omit option
        sys.argv = ['cl.py', '--search', '--omit_ingredients', 'Ingredient1']
        sys.stdout = StringIO()

        main()

        expected_recipes = "Searching for recipes...\n" \
            "['1', 'Title2', 'Instructions for Title2', ['Ingredient3', 'Ingredient4']]\n" \
            "['2', 'Title3', 'Instructions for Title3', ['Ingredient5', 'Ingredient6']]\n" \
            "['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']]\n" \
            "['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']]\n" \
            "['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']]\n" \
            "['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']]\n" \
            "['7', 'Title8', 'Instructions for Title8', "\
            "['Ingredientf', 'Ingredientg', 'Ingredient3']]\n" \
            "['9', 'Title10', 'Instructions for Title10', " \
            "['Ingredient4', 'Ingredient8', 'Ingrediente']]"
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_recipes, "Should be the same")

    def test_command_line_help(self):
        '''
        Tests the command line interface.
        '''

        # Test the command line interface with the --help option
        sys.argv = ['cl.py', '--help']
        sys.stdout = StringIO()

        main()

        expected_output = "Displaying help...\nUsage: python cl.py --search " \
        "--include_ingredients <ingredients> --omit_ingredients <ingredients>\n" \
        "<ingredients> should be a comma-separated list of ingredients enclosed " \
        "in quotes.\nor python cl.py --random <number>\nor python cl.py --help\n" \
        "--search or --s: Search for a specific recipe.\n--random or --r: Get a " \
        "random recipe.\n--help or --h: Display this help message."

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_output, "Should be the same")


if __name__ == "__main__":
    unittest.main()
