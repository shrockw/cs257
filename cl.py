'''
This file is the command line interface for the project.
'''
from ProductionCode.recipe_search import find_recipes
from ProductionCode.random_recipe import get_random_recipes
from ProductionCode.data import get_data
import sys


def main():
    ''' Main function to handle command line arguments and execute the appropriate function. '''
    if len(sys.argv) < 2:
        usage_statement()
    if len(sys.argv) > 6:
        usage_statement()
    command = sys.argv[1]

    if command == "--search":
        print("Searching for recipes...")
        search()
    elif command == "--random":
        print("Getting random recipe...")
        if len(sys.argv) != 3:
            print("Invalid number of arguments for --random.")
            usage_statement()
        random_cl()
    elif command == "--help":
        print("Displaying help...")
        help_cl()
    else:
        print("Invalid command. Use --help for usage information.")


def usage_statement():
    ''' Display the usage statement for the command line interface. '''
    print("Usage: python cl.py --search --include_ingredients <ingredients> --omit_ingredients <ingredients>")
    print("or python cl.py --random <number>")
    print("or python cl.py --help")


def search():
    ''' Search for recipes based on the given ingredients. '''
    recipe_data = get_data("test_data.csv", "Data")
    include_ingredients = sys.argv[sys.argv.index(
        "--include_ingredients") + 1].split(", ") if "--include_ingredients" in sys.argv else []
    omit_ingredients = sys.argv[sys.argv.index(
        "--omit_ingredients") + 1].split(",") if "--omit_ingredients" in sys.argv else []
    recipes = find_recipes(recipe_data, include_ingredients, omit_ingredients)
    print(recipes)
    return recipes


def random_cl():

    ''' Get a random n number of recipes.'''
    recipe_data = get_data("test_data.csv", "Data")
    num = int(sys.argv[2])
    recipe_data = recipe_data[1:]
    random_recipes = get_random_recipes(recipe_data, num)
    print(random_recipes)
    return random_recipes


def help_cl():
    ''' Display the help information for the command line interface. '''
    print("Usage: python cl.py --search --include_ingredients <ingredients> --omit_ingredients <ingredients>")
    print("or python cl.py --random <number>")
    print("or python cl.py --help")
    print("--search: Search for a specific recipe.")
    print("--random: Get a random recipe.")
    print("--help: Display this help message.")


if __name__ == "__main__":
    main()
