'''This module contains the DataSource class that handles database connections and queries.'''

import sys
import ast
import psycopg2
import ProductionCode.psql_config as config

class DataSource:
    '''This class handles the connection to the PostgreSQL database 
    and provides methods to query recipes.'''

    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.'''

        try:
            connection = psycopg2.connect(database=config.DATABASE, user=config.USER,
                password=config.PASSWORD, host="localhost")
        except psycopg2.Error as e:
            print("Connection error: ", e)
            sys.exit(1)
        return connection

    def get_all_recipes(self):
        '''Returns all recipes from the database'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title FROM recipe ORDER BY title")
        records = [self.convert_recipe_to_object(record) for record in cursor.fetchall()]
        cursor.close()

        return records

    def get_recipe_by_ingredients(self, include_ingredients, exclude_ingredients):
        '''Fetches recipes that include certain ingredients and exclude others'''
        cursor = self.connection.cursor()

        query = "SELECT id, title FROM recipe WHERE "
        conditions = []
        params = []


        if include_ingredients:
            for ingredient in include_ingredients:
                conditions.append("ingredients ILIKE %s")
                params.append(f"%{ingredient}%")

        if exclude_ingredients:
            for ingredient in exclude_ingredients:
                conditions.append("ingredients NOT ILIKE %s")
                params.append(f"%{ingredient}%")

        if conditions:
            query += " AND ".join(conditions)
        else:
            return []

        query += " ORDER BY title;"


        cursor.execute(query, params)
        records = [self.convert_recipe_to_object(record) for record in cursor.fetchall()]
        cursor.close()
        return records

    def get_random_recipes(self, number):
        ''' This function retrieves random recipes from the database.
        Args:
        number: number of random recipes to retrieve
        Returns a list of tuples containing the data.
        '''
        query = "SELECT id, title FROM recipe ORDER BY RANDOM() LIMIT %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (number,))
        records = [self.convert_recipe_to_object(record) for record in cursor.fetchall()]
        cursor.close()
        return records

    def get_recipe_by_title(self, title):
        '''This function retrieves the recipe ID based on the recipe title.
        Args:
        title: title of the recipe
        Returns the recipe ID.
        '''
        cursor = self.connection.cursor()
        query = "SELECT * FROM recipe WHERE title = %s"
        cursor.execute(query, (title,))
        recipe = self.convert_recipe_to_object(cursor.fetchone())
        cursor.close()
        return recipe if recipe else None

    def convert_recipe_to_object(self, recipe):
        '''This function converts the recipe data into a Recipe object.
        Args:
        recipe: tuple containing the recipe data
        Returns a Recipe object.
        '''
        if len(recipe) == 2:
            recipe_id, title = recipe
            return Recipe(recipe_id, title)
        if len(recipe) == 4:
            recipe_id, title, instructions, ingredients = recipe
            return Recipe(recipe_id, title, instructions, ingredients)
        
        raise ValueError("Invalid recipe data format")

    def get_recipe_by_id(self, recipe_id):
        '''This function retrieves the recipe data based on the recipe ID.
        Args:
        recipe_id: ID of the recipe
        Returns the recipe data.
        '''
        cursor = self.connection.cursor()
        query = "SELECT * FROM recipe WHERE id = %s"
        cursor.execute(query, (recipe_id,))
        recipe = self.convert_recipe_to_object(cursor.fetchone())
        cursor.close()
        return recipe

    def get_all_recipe_titles(self):
        '''This function retrieves all recipe titles from the database.
        Returns a list of recipe titles.
        '''
        cursor = self.connection.cursor()
        query = "SELECT title FROM recipe"
        cursor.execute(query)
        titles = cursor.fetchall()
        cursor.close()
        return [title[0] for title in titles]

    def get_instructions_and_ingredients(self, recipe_id):
        '''This function retrieves the instructions and ingredients of a recipe 
        based on the recipe ID.'''
        cursor = self.connection.cursor()
        query = "SELECT instructions, ingredients FROM recipe WHERE id = %s"
        cursor.execute(query, (recipe_id,))
        instructions, ingredients = cursor.fetchone()
        cursor.close()
        return instructions, ingredients



class Recipe():
    '''This class represents a recipe object. It contains methods to get the title, 
    ingredients, and instructions of the recipe.'''

    def __init__(self, recipe_id, recipe_title, recipe_instructions=None, recipe_ingredients=None):
        '''Constructor that initializes the recipe object with the given recipe data.'''
        self.recipe_id = recipe_id
        self.title = recipe_title
        if recipe_instructions is not None:
            self.instructions = recipe_instructions.split("\n")
        else:
            self.instructions = recipe_instructions
        if recipe_ingredients is not None:
            self.ingredients = ast.literal_eval(recipe_ingredients)
        else:
            self.ingredients = recipe_ingredients

    def get_id(self):
        '''Returns the ID of the recipe.'''
        return self.recipe_id

    def get_title(self):
        '''Returns the title of the recipe.'''
        return self.title

    def get_instructions(self):
        '''Returns the instructions of the recipe.'''
        if self.instructions is None:
            self.find_instructions_and_ingredients()
        return self.instructions

    def get_ingredients(self):
        '''Returns the ingredients of the recipe.'''
        if self.ingredients is None:
            self.find_instructions_and_ingredients()
        return self.ingredients

    def find_instructions_and_ingredients(self):
        '''Returns the instructions of the recipe.'''
        recipe_data = DataSource()
        additional_recipe_info = recipe_data.get_instructions_and_ingredients(self.recipe_id)
        self.instructions = additional_recipe_info[0].split("\n")
        self.ingredients = ast.literal_eval(additional_recipe_info[1])
