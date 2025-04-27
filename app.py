'''
The eventual location for the Flask app interface for the project.
'''

from flask import Flask
from ProductionCode.random_recipe import get_random_recipes
from ProductionCode.data import get_data
from ProductionCode.recipe_search import find_recipes

app = Flask(__name__)

@app.route('/')
def homepage():
    '''This function returns the homepage.'''
    return "In the url after the /, \
        enter the word random, then a /, \
        then a number between 1 and 10. \
        This will return that many random recipes from the dataset. \
        For example: /random/3 will return 3 random recipes. <br><br> \
        Or to search for recipes with specific ingredients, \
        use /search/include/ingredient1,ingredient2,ingredient3. \
        To omit ingredients, use /search/omit/ingredient1,ingredient2,ingredient3. <br><br> \
        You can also use /search/include/ingredient1,ingredient2/omit/ingredient3. "

@app.route('/random/<int:num_recipes>')
def random_recipes(num_recipes):
    '''This function returns a random recipe from the dataset.'''
    if num_recipes < 1 or num_recipes > 10:
        return "Please enter a number between 1 and 10."
    # Call the function to get random recipes here
    recipe_data = get_data("recipe_data.csv", "Data")
    recipe_data = recipe_data[1:]
    randrecipes = get_random_recipes(recipe_data, num_recipes)
    output = ""
    for recipe in randrecipes:
        output += f"{recipe[1]}: {recipe[2]}<br><br>"
    # return str(recipes)
    return f"Returning {num_recipes} random recipes...<br><br> {output}"

@app.route('/search/include/<string:ingredients>')
def search_include(ingredients):
    '''This function searches for recipes that include the specified ingredients.'''
    recipe_data = get_data("recipe_data.csv", "Data")
    recipe_data = recipe_data[1:]
    include_ingredients = ingredients.split(",")
    recipes = find_recipes(recipe_data, include_ingredients, [])
    output = ""
    for recipe in recipes:
        output += f"{recipe[1]}: {recipe[2]}<br><br>"
    return f"Recipes including {include_ingredients}:<br><br> {output}"

@app.route('/search/omit/<string:ingredients>')
def search_omit(ingredients):
    '''This function searches for recipes that omit the specified ingredients.'''
    recipe_data = get_data("recipe_data.csv", "Data")
    recipe_data = recipe_data[1:]
    omit_ingredients = ingredients.split(",")
    recipes = find_recipes(recipe_data, [], omit_ingredients)
    output = ""
    for recipe in recipes:
        output += f"{recipe[1]}: {recipe[2]}<br><br>"
    return f"Recipes omitting {omit_ingredients}:<br><br> {output}"

@app.route('/search/include/<string:include_ingredients>/omit/<string:omit_ingredients>')
def search_include_omit(include_ingredients, omit_ingredients):
    '''This function searches for recipes that include and omit the specified ingredients.'''
    recipe_data = get_data("recipe_data.csv", "Data")
    recipe_data = recipe_data[1:]
    include_ingredients = include_ingredients.split(",")
    omit_ingredients = omit_ingredients.split(",")
    recipes = find_recipes(recipe_data, include_ingredients, omit_ingredients)
    output = ""
    for recipe in recipes:
        output += f"{recipe[1]}: {recipe[2]}<br><br>"
    return f"Recipes including {include_ingredients} and omitting {omit_ingredients}: \
        <br><br> {output}"

@app.errorhandler(404)
def page_not_found(e):
    '''This function handles 404 errors, which are page not found errors.'''
    return f"Sorry, wrong format. Do this instead: the_url/random/number_of_recipes or <br><br> \
        the_url/search/include/[ingredients separated by commas] or <br><br> \
        the_url/search/omit/[ingredients separated by commas] or <br><br> \
        the_url/search/[ingredients separated by commas]/omit/[ingredients separated by commas] \
            {str(e)}"

@app.errorhandler(500)
def python_bug(e):
    '''This function handles 500 errors, which are internal server errors.'''
    return f"A bug! {str(e)}"

if __name__ == '__main__':
    app.run()
