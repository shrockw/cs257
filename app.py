'''
This is the main file for the Flask web application.
It handles the routing and serves the web pages.
'''

from flask import Flask
from ProductionCode.datasource import DataSource

app = Flask(__name__)

TOTAL_NUM_RECIPES = 13501

@app.route('/')
def homepage():
    '''This function returns the homepage.'''
    return "In the url after the /, enter the word random, then a /, then a number " \
    "between 1 and 13501. This will return that many random recipes from the dataset. " \
    "For example: /random/3 will return 3 random recipes. <br><br> Or to search for " \
    "recipes with specific ingredients, use /search/include/ingredient1,ingredient2,ingredient3. " \
    "To omit ingredients, use /search/omit/ingredient1,ingredient2,ingredient3. " \
    "<br><br> You can also use /search/include/ingredient1,ingredient2/omit/ingredient3. "

@app.route('/all_recipes')
def all_recipes():
    '''This function returns all recipes in the dataset.'''
    recipe_data = DataSource()
    recipes = recipe_data.get_all_recipes()
    output = build_output_string(recipes)
    return f"Returning all recipes...<br><br> {output}"

@app.route('/random/<int:num_recipes>')
def random_recipes(num_recipes):
    '''Fetches n random recipes from the dataset separated by line breaks.
    Args:
        num_recipes: number of recipes to return (must be between 1 and 13501)
    Returns:
        A string contain the recipes separated by line breaks
    '''
    if num_recipes < 1 or num_recipes > TOTAL_NUM_RECIPES:
        return "Please enter a valid number between 1 and 13501."

    recipe_data = DataSource()
    recipes = recipe_data.get_random_recipes(num_recipes)
    output = build_output_string(recipes)
    return f"Returning {num_recipes} random recipes...<br><br> {output}"

def build_output_string(recipes):
    '''Helper function to build the output string from the list of recipes.
    Args:
        recipes: list of tuples containing the recipe data
    Returns:
        A string containing the recipe names and their descriptions
    '''
    output = ""
    for recipe in recipes:
        output += f"{recipe[1]}: {recipe[2]}<br><br>"
    return output

@app.route('/search', defaults={'include_ingredients': None, 'omit_ingredients': None})
@app.route('/search/include/<string:include_ingredients>', defaults={'omit_ingredients': None})
@app.route('/search/omit/<string:omit_ingredients>', defaults={'include_ingredients': None})
@app.route('/search/include/<string:include_ingredients>/omit/<string:omit_ingredients>')
def search_include_omit(include_ingredients, omit_ingredients):
    '''This function searches for recipes that include and omit the specified ingredients
    and returns the recipes that satisfy these parameters in specified format.
    Args:
        include_ingredients: list of ingredients to include (optional)
        omit_ingredients: list of ingredients to omit (optional)
    Returns:
        A string containing the recipes that satisfy the parameters
    '''
    recipe_data = DataSource()
    if include_ingredients:
        parsed_include_ingredients = parse_ingredients(include_ingredients)
    else:
        parsed_include_ingredients = []
    if omit_ingredients:
        parsed_omit_ingredients = parse_ingredients(omit_ingredients)
    else:
        parsed_omit_ingredients = []
    recipes = recipe_data.get_recipe_by_ingredients(parsed_include_ingredients,\
                                                     parsed_omit_ingredients)
    output = build_output_string(recipes)
    return f"Recipes including {include_ingredients} and omitting {omit_ingredients}: \
        <br><br> {output}"

def parse_ingredients(ingredients):
    '''This function parses the ingredients from the URL into a list of ingredients.
    Args:
        ingredients: string of ingredients separated by commas
    Returns:
        A list of ingredients
    '''
    return ingredients.split(",")

@app.errorhandler(404)
def page_not_found(e):
    '''This function handles 404 errors with helpful usage suggestions.'''
    return f"""
    <h1>Oops! Page not found</h1>
    <p>Sorry, the URL you requested could not be found.</p>
    <p>Here are some ways you can use this application:</p>
    <ul>
        <li><strong>Get a random number recipes:</strong><br> 
            the_url/random/number_of_recipes<br>
            Example: <code>the_url/random/3</code>
        </li><br>
        <li><strong>Search for recipes by included ingredients:</strong><br>
            the_url/search/include/[ingredients separated by commas]<br>
            Example: <code>the_url/search/include/chicken,rice</code>
        </li><br>
        <li><strong>Search for recipes omitting certain ingredients:</strong><br>
            the_url/search/omit/[ingredients separated by commas]<br>
            Example: <code>the_url/search/omit/onion,garlic</code>
        </li><br>
        <li><strong>Search by included and omitted ingredients:</strong><br>
            the_url/search/include/[included ingredients]/omit/[omitted ingredients]<br>
            Example: <code>the_url/search/include/chicken,rice/omit/onion,garlic</code>
        </li>
    </ul>
    <p>{str(e)}</p>
    """

@app.errorhandler(500)
def python_bug(e):
    '''This function handles 500 errors, which are internal server errors.'''
    return f"A bug! {str(e)}"

if __name__ == '__main__':
    app.run()
