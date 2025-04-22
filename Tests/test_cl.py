'''
Contains tests for the command line interface of the program.
'''

import unittest
import sys
from io import StringIO
import ast
import random
from ProductionCode.data import get_data, get_filepath
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

        expected_data_file_path = get_filepath("loaded_data_test.txt", "Tests")

        with open(expected_data_file_path, "r", encoding="utf-8") as f:
            expected_data = f.readlines()[0]

        self.assertEqual(get_data("test_data.csv", "Data"),
                         ast.literal_eval(expected_data), "Should be the same")


class TestRandomRecipe(unittest.TestCase):
    '''
    Tests the random recipe function.
    '''

    def setUp(self):
        random.seed(931254)

    def test_random_recipe(self):
        '''
        Tests the random recipe function.
        '''

        expected_recipes = [['9', 'Title10', 'Instructions for Title10', [
            'Ingredient4', 'Ingredient8', 'Ingrediente']]]
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(get_random_recipes(test_recipes, 1),
                         expected_recipes, "Should be the same")

        expected_recipes = [['6', 'Title7', 'Instructions for Title7',
                             ['Ingredientd', 'Ingrediente']],
                            ['3', 'Title4', 'Instructions for Title4',
                             ['Ingredient7', 'Ingredient8']],
                            ['7', 'Title8', 'Instructions for Title8',
                             ['Ingredientf', 'Ingredientg', 'Ingredient3']]]
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(get_random_recipes(test_recipes, 3),
                         expected_recipes, "Should be the same")

        expected_recipes = []
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(get_random_recipes(test_recipes, 0),
                         expected_recipes, "Should be the same")

    def test_random_recipe_invalid(self):
        '''
        Tests the random recipe function with invalid input.
        '''

        test_recipes = get_data("test_data.csv", "Data")
        with self.assertRaises(ValueError):
            get_random_recipes(test_recipes, -1)

        with self.assertRaises(ValueError):
            get_random_recipes(test_recipes, 100)


class TestRecipeSearch(unittest.TestCase):
    '''
    Tests the recipe search function.
    '''

    def test_recipe_search_wanted(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [['0', 'Title1', 'Instructions for Title1',
                             ['Ingredient1', 'Ingredient2']],
                            ['8', 'Title9', 'Instructions for Title9',
                             ['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']]]
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, ["Ingredient1"], [
        ]), expected_recipes, "Should be the same")

        expected_recipes = []
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, ["Ingredient1", "Ingredient3"], [
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
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, ["Ingredient"], [
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
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, [], [
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
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, [], [
                         "Ingrediente", "Ingredient9"]), expected_recipes, "Should be the same")

        expected_recipes = []
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, [], [
                         "Ingredient"]), expected_recipes, "Should be the same")

    def test_recipe_search_both(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [
            ['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']]]

        test_recipes = get_data("test_data.csv", "Data")

        self.assertEqual(find_recipes(test_recipes, ["Ingredient1", "Ingredient2"], [
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
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, [], []),
                         expected_recipes, "Should be the same")

        expected_recipes = []
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, ["Ingredient"], [
                         "Ingredient"]), expected_recipes, "Should be the same")

        expected_recipes = []
        test_recipes = get_data("test_data.csv", "Data")
        self.assertEqual(find_recipes(test_recipes, ["Ingredient4"], [
                         "Ingredient4"]), expected_recipes, "Should be the same")


class TestCommandLine(unittest.TestCase):
    '''
    Tests the command line interface.
    '''

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
