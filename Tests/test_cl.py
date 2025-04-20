'''
Contains tests for the command line interface of the program.
'''

import unittest
import sys
from io import StringIO
import os
import ast
import random
from ProductionCode.data import get_data, get_filepath
from ProductionCode.recipe_search import find_recipes
from ProductionCode.random_recipe import get_random_recipes


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

    def test_random_recipe(self):
        '''
        Tests the random recipe function.
        '''

        expected_recipe = [['9','Title10','Instructions for Title10',['Ingredient4', 'Ingredient8', 'Ingrediente']]]

        test_recipes = get_data("test_data.csv", "Data")

        random.seed(32719)

        self.assertEqual(get_random_recipes(test_recipes, 1), expected_recipe, "Should be the same")



class TestRecipeSearch(unittest.TestCase):
    '''
    Tests the recipe search function.
    '''

    def test_recipe_search_wanted(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']], ['8','Title9','Instructions for Title9',['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']]]

        test_recipes = get_data("test_data.csv", "Data")

        self.assertEqual(find_recipes(test_recipes, ["Ingredient1"], []), expected_recipes, "Should be the same")




    def test_recipe_search_unwanted(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']], ['1', 'Title2', 'Instructions for Title2', ['Ingredient3', 'Ingredient4']], ['3', 'Title4', 'Instructions for Title4', ['Ingredient7', 'Ingredient8']], ['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredienta']], ['5', 'Title6', 'Instructions for Title6', ['Ingredientb', 'Ingredientc']], ['6', 'Title7', 'Instructions for Title7', ['Ingredientd', 'Ingrediente']], ['7','Title8','Instructions for Title8',['Ingredientf', 'Ingredientg', 'Ingredient3']], ['8','Title9','Instructions for Title9',['Ingredienth', 'Ingredienti', 'Ingredient7', 'Ingredient1']], ['9','Title10','Instructions for Title10',['Ingredient4', 'Ingredient8', 'Ingrediente']]]
        test_recipes = get_data("test_data.csv", "Data")

        self.assertEqual(find_recipes(test_recipes, [], ["Ingredient5"]), expected_recipes, "Should be the same")

    def test_recipe_search_both(self):
        '''
        Tests the recipe search function.
        '''

        expected_recipes = [['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']]]

        test_recipes = get_data("test_data.csv", "Data")

        self.assertEqual(find_recipes(test_recipes, ["Ingredient1", "Ingredient2"], ["Ingredient11"]), expected_recipes, "Should be the same")

        
class TestCommandLine(unittest.TestCase):
    '''
    Tests the command line interface.
    '''
    def test_command_line_random(self);
        sys.argv = ['cl.py', '--random', '3']
        sys.stdout = StringIO()
        test_recipes = get_data("test_data.csv", "Data")

        expected_recipe = ['4', 'Title5', 'Instructions for Title5', ['Ingredient9', 'Ingredient10']]

        random.seed(32719)

        produced = #get_random_recipe(test_recipes, 3)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, produced, "Should be the same")
    
    def test_command_line_include(self):
        '''
        Tests the command line interface.
        '''

        # Test the command line interface with the --include option
        sys.argv = ['cl.py', '--include', 'Ingredient1, Ingredient2']
        sys.stdout = StringIO()
        test_recipes = get_data("test_data.csv", "Data")
        produced = #find_recipes(test_recipes, ["Ingredient1", "Ingredient2"], [])

        expected_recipes = [['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']]]

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, produced, "Should be the same")

        # Test the command line interface with the --omit option
        sys.argv = ['cl.py', '--include', 'Ingredient1', '--omit', 'Ingredient2']
        sys.stdout = StringIO()
        test_recipes = get_data("test_data.csv", "Data")
        produced = #find_recipes(test_recipes, ["Ingredient1"], ["Ingredient2"])

        expected_recipes = [['0', 'Title1', 'Instructions for Title1', ['Ingredient1', 'Ingredient2']]]

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, produced, "Should be the same")

if __name__ == "__main__":
    unittest.main()
