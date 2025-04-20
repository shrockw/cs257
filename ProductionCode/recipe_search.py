'''This file deals with the recipe search function'''

def find_recipes(recipe_data, wanted_ingredients, unwanted_ingredients):
    '''Find recipes that match the wanted and unwanted ingredients.'''
    matching_recipes = []
    for recipe in recipe_data:
        if valid_recipe(recipe, wanted_ingredients, unwanted_ingredients):
            matching_recipes.append(recipe)
    return matching_recipes

def valid_recipe(recipe, wanted_ingredients, unwanted_ingredients):
    '''Check if a recipe is valid based on the wanted and unwanted ingredients.'''
    for ingredient in wanted_ingredients:
        if ingredient not in recipe[3]:
            return False
    for ingredient in unwanted_ingredients:
        if ingredient in recipe[3]:
            return False
    return True


# def parse_ingredient(ingredients):
#     '''Parse a string of ingredients into a list.'''
#     ingredient_list = ingredients.split(", ")
#     return ingredient_list

# def search_recipes(ingredient_list, recipe_data):
#     '''Search for recipes that contain all the ingredients in the ingredient list.'''
#     matching_recipes = []
#     for recipe in recipe_data:
#         if all(ingredient in recipe['ingredients'] for ingredient in ingredient_list):
#             matching_recipes.append(recipe)
#     return matching_recipes