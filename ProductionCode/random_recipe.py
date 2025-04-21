import random
# from data import get_data

def get_random_recipes(recipes, num_recipes):
    """
    Returns a random recipe from the given list of recipes.
    """

    return random.sample(recipes, num_recipes)

# if __name__ == "__main__":
#     # Example usage
#     random.seed(32719)  # Set a seed for reproducibility

#     a = get_data("test_data.csv", "Data")
#     random_recipes = get_random_recipes(a, 3)
#     print(random_recipes)