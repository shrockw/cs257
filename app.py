'''
This is the main file for the Flask web application.
It handles the routing and serves the web pages.
'''


from flask import Flask, render_template, request, redirect, url_for, jsonify
import string
from ProductionCode.datasource import DataSource, Recipe


app = Flask(__name__)

TOTAL_NUM_RECIPES = 13501

@app.route('/')
def homepage():
    '''This function returns the homepage.'''
    recipe_data = DataSource()
    featured_recipe = recipe_data.get_random_recipes(1)
    marc_recipe = recipe_data.get_recipe_by_id(9877)
    willan_recipe = recipe_data.get_recipe_by_id(2)
    anika_recipe = recipe_data.get_recipe_by_id(3)
    allison_recipe = recipe_data.get_recipe_by_id(4)
    return render_template('homepage.html', featured_recipe=featured_recipe[0], 
                           marc_recipe=marc_recipe,
                           willan_recipe=willan_recipe, 
                           anika_recipe=anika_recipe,
                           allison_recipe=allison_recipe)


@app.route('/random', methods=['GET', 'POST'])
def random():
    if request.method == 'POST':
        recipe_data = DataSource()
        num = int(request.form.get('num_recipes', 1))
        recipes = recipe_data.get_random_recipes(num)


        # Directly pass recipes to the template
        simplified_recipes = [(r.get_id(), r.get_title()) for r in recipes]  # (id, title)
        return render_template('recipelist.html', recipes=simplified_recipes)

    return render_template('random.html')

@app.route('/custom', methods=['GET', 'POST'])
def custom_search():
    """Handle ingredient search form submission"""
    if request.method == 'POST':
        recipe_data = DataSource()
        
        include = request.form.get('include_ingredients', '').split(',')
        exclude = request.form.get('exclude_ingredients', '').split(',')
        
        include = [i.strip().lower() for i in include if i.strip()]
        exclude = [e.strip().lower() for e in exclude if e.strip()]
        
        recipes = recipe_data.get_recipe_by_ingredients(include, exclude)
        
        simplified_recipes = [(r[0], r[1]) for r in recipes]
        return render_template('found_recipes.html', recipes=simplified_recipes)
    
    return render_template('custom.html')

@app.route('/all_recipes')
def all_recipes():
    recipe_data = DataSource()
    recipes = recipe_data.get_all_recipes()
    sorted_recipes = sort_recipes_alphabetically(recipes)
    return render_template('all_recipes.html', sorted_recipes = sorted_recipes, letters = string.ascii_uppercase)

def sort_recipes_alphabetically(recipes):
    sorted_recipes = []
    for letter in string.ascii_lowercase:
        current_letter = (letter.upper(), [])
        for recipe in recipes:
            title = recipe.get_title()
            if title.lower().startswith(letter):
                current_letter[1].append((recipe.get_id(), title))

        sorted_recipes.append(current_letter)

    return sorted_recipes

        

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

@app.route('/search_by_title')
def search_by_title(last_search=None):
    '''Route to display the search by title page from search_by_title.html
    Arguments: 
        last_search: The last searched recipe title which is None unless the last search did not 
        exist in the database.
    Returns:
        Renders the search by title template.
    '''
    return render_template('search_by_title.html', last_search=last_search)

@app.route('/find_recipe_by_title', methods=['POST'])
def find_recipe_by_title():
    '''Route to handle the search by title form submission.
    Arguments:
        None
    Returns:
        Redirects to the display_recipe route if the recipe is found, otherwise redirects to the 
        search_by_title route with the last search.
    '''
    searched_title = request.form.get('recipe_title')
    recipe_data = DataSource()
    recipe = recipe_data.get_recipe_by_title(searched_title)
    if recipe:
        return redirect(url_for('display_recipe', recipe_id=recipe.get_id()))
    return search_by_title(last_search=searched_title)

@app.route('/display_recipe/<recipe_id>')
def display_recipe(recipe_id):
    '''Route to display the recipe details using display_recipe.html
    Arguments:
        recipe_id: The ID of the recipe to be displayed.
    Returns:
        Renders the display recipe template with the recipe details.
    '''
    recipe_data = DataSource()
    recipe = recipe_data.get_recipe_by_id(recipe_id)
    if recipe:
        return render_template('display_recipe.html',
                               recipe_title=recipe.get_title(),
                               recipe_ingredients=recipe.get_ingredients(),
                               recipe_instructions=recipe.get_instructions())

    return render_template('recipe_not_found_error.html')

@app.route('/autocomplete')
def autocomplete():
    '''Route to handle the autocomplete functionality for recipe titles.
    Arguments:
        None
    Returns:
        Returns a JSON response with the list of suggestions based on the query parameter.
    '''
    query = request.args.get('cur_search')
    recipe_data = DataSource()
    autocomplete_data = recipe_data.get_all_recipe_titles()
    print([a for a in autocomplete_data if a == None])
    # print(autocomplete_data)
    if query:
        suggestions = [item for item in autocomplete_data if query.lower() in item.lower()]
        return jsonify(suggestions)
    return jsonify([])

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
    app.run(port = 5002)
