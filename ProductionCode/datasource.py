'''This module contains the DataSource class that handles database connections and queries.'''

import sys
import psycopg2
import ProductionCode.psqlconfig as config

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
        cursor.execute("SELECT * FROM recipe")
        records = cursor.fetchall()

        return records

    def get_recipe_by_ingredients(self, include_ingredients, exclude_ingredients):
        '''Fetches recipes that include certain ingredients and exclude others. 
        Returns a list of tuples containing the data.'''

        cursor = self.connection.cursor()
        query = self.create_recipe_by_ingredients_query(include_ingredients, exclude_ingredients)
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        return data
    
    def create_recipe_by_ingredients_query(self, include_ingredients, exclude_ingredients):
        '''Creates a SQL query to fetch recipes based on included and excluded ingredients.'''
        query = "SELECT * FROM recipe WHERE "
        if include_ingredients:
            query += " AND ".join(
                [f"ingredients ILIKE '%{ingredient}%'" for ingredient in include_ingredients])
            if exclude_ingredients:
                query += f" AND "
        query += " AND ".join(
            [f"ingredients NOT ILIKE '%{ingredient}%'" for ingredient in exclude_ingredients])
        return query

    def get_random_recipes(self, number):
        ''' This function retrieves random recipes from the database. '''
        query = "SELECT * FROM recipe ORDER BY RANDOM() LIMIT %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (number,))
        records = cursor.fetchall()
        cursor.close()
        return records

