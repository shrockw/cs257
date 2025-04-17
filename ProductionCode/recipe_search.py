'''This file deals with the recipe search function'''

def parse_ingredient(ingredients):
    '''Parse a string of ingredients into a list.'''
    ingredient_list = ingredients.split(", ")
    return ingredient_list

def search_recipes(ingredient_list, recipe_data):
    '''Search for recipes that contain all the ingredients in the ingredient list.'''
    matching_recipes = []
    for recipe in recipe_data:
        if all(ingredient in recipe['ingredients'] for ingredient in ingredient_list):
            matching_recipes.append(recipe)
    return matching_recipes