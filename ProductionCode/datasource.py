'''This module contains the DataSource class that handles database connections and queries.'''

import sys
import psycopg2
import ProductionCode.psqlConfig as config

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
            connection = psycopg2.connect(database=config.database, user=config.user,
                password=config.password, host="localhost")
        except psycopg2.Error as e:
            print("Connection error: ", e)
            sys.exit(1)
        return connection

    def get_all_recipes(self):
        '''Returns all recipes from the database'''
        #Open a cursor to perform database operations
        cursor = self.connection.cursor()

        #Execute a query
        cursor.execute("SELECT * FROM recipe")

        #Retrieve query results
        records = cursor.fetchall()

        print(records)

    def get_recipe_with(self, included_ingredients):
        '''Returns a list of recipes that contain all specified ingredients'''
        cursor = self.connection.cursor()

        query = "SELECT * FROM recipe WHERE "
        conditions = []
        values = []

        for ingredient in included_ingredients:
            conditions.append("ingredients LIKE %s")
            values.append(f"%{ingredient}%")

        query += " AND ".join(conditions)

        cursor.execute(query, values)
        recipes = cursor.fetchall()
        return [recipe[0] for recipe in recipes]

    def get_random_recipes(self, number):
        ''' This function retrieves random recipes from the database. '''
        query = "SELECT * FROM recipes ORDER BY RANDOM() LIMIT %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (number,))
        records = cursor.fetchall()
        return [recipe[0] for recipe in recipes]
