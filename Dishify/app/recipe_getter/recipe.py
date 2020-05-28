from recipe_scrapers import scrape_me
from recipe_getter.recipe_helper import parse_ingredients_mod
import json





def get_recipe(url):

    """
    function to scrape a recipe with a given url and return the content in 
    a ordered way as a JSON
    """

    try:

        # list to store all parts of the recipe
        complete_recipe = []

        # query the given url
        scraper = scrape_me(url)

        # append the title of the recipe
        complete_recipe.append({"title":scraper.title()})

        # parse ingredients

        ingredients_dict = parse_ingredients_mod(scraper)
        complete_recipe.append(ingredients_dict)

        # parse instructions

        instructions_list = scraper.instructions().splitlines()
        complete_recipe.append({"instructions":instructions_list})

        return json.dumps({"recipe":complete_recipe})

    except Exception as e:
        return json.dumps({"error":f"{e}"})





    