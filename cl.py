'''
This file is the command line interface for the project.
'''
import sys
from ProductionCode.recipe_search import find_recipes
from ProductionCode.random_recipe import get_random_recipes
from ProductionCode.data import get_data


def main():
    ''' Main function to handle command line arguments and execute the appropriate function. '''
    if len(sys.argv) < 2:
        usage_statement()
    if len(sys.argv) > 6:
        usage_statement()
    command = sys.argv[1]

    if command in ("--search", "--s"):
        print("Searching for recipes...")
        search()
    elif command in ("--random", "--r"):
        print("Getting random recipe...")
        if len(sys.argv) != 3:
            print("Invalid number of arguments for --random.")
            usage_statement()
        random_cl()
    elif command in ("--help", "--h"):
        print("Displaying help...")
        help_cl()
    else:
        print("Invalid command. Use --help for usage information.")


def usage_statement():
    ''' Display the usage statements for the command line interface. '''
    print("Usage: python cl.py --search --include_ingredients\
    <ingredients> --omit_ingredients <ingredients>")
    print("<ingredients> should be a comma-separated list\
           of ingredients enclosed in quotes.")
    print("or python cl.py --random <number>")
    print("or python cl.py --help")
    print("--search or --s: Search for a specific recipe.")
    print("--random or --r: Get a random recipe.")
    print("--help or --h: Display help message.")


def search():
    ''' Search for recipes based on the given ingredients. '''
    recipe_data = get_data("test_data.csv", "Data")
    include_ingredients = get_included_ingredients()
    omit_ingredients = get_omitted_ingredients()
    recipes = find_recipes(recipe_data, include_ingredients, omit_ingredients)
    print_recipes(recipes)
    return recipes

def print_recipes(recipes):
    ''' Print the recipes found line by line. '''
    for recipe in recipes:
        print(recipe)

def get_included_ingredients():
    ''' Get the included ingredients from the command line arguments. '''
    if "--include_ingredients" in sys.argv:
        index = sys.argv.index("--include_ingredients") + 1
        return sys.argv[index].split(", ")
    return []

def get_omitted_ingredients():
    ''' Get the omitted ingredients from the command line arguments. '''
    if "--omit_ingredients" in sys.argv:
        index = sys.argv.index("--omit_ingredients") + 1
        return sys.argv[index].split(", ")
    return []


def random_cl():
    ''' Get a random n number of recipes.'''
    recipe_data = get_data("test_data.csv", "Data")
    num = int(sys.argv[2])
    recipe_data = recipe_data[1:]
    random_recipes = get_random_recipes(recipe_data, num)
    print_recipes(random_recipes)
    return random_recipes


def help_cl():
    ''' Display the help information for the command line interface. '''
    print("Usage: python cl.py --search --include_ingredients \
          <ingredients> --omit_ingredients <ingredients>")
    print("<ingredients> should be a comma-separated list of ingredients enclosed in quotes.")
    print("or python cl.py --random <number>")
    print("or python cl.py --help")
    print("--search or --s: Search for a specific recipe.")
    print("--random or --r: Get a random recipe.")
    print("--help or --h: Display this help message.")


if __name__ == "__main__":
    main()
