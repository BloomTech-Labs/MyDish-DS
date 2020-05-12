from flask import Blueprint
from app.route.recipe_parser.helper import decode_string_and_api_call
from app.route.recipe_parser.ingredients import parse_ingredients
from app.route.recipe_parser.instructions import parse_instructions
from app.route.ingredients_populater.getter import ingredient_getter
from pydantic import BaseModel


all_routes = Blueprint("all_routes", __name__)


class ImageJson(BaseModel):
    image: str


class StringJson(BaseModel):
    word: str


@all_routes.route("/recipe_parser/ingredients")
def ingredients(item: ImageJson):
    """
        ???????????
        takes in a Json, decodes the string in it to a picture, makes a vision api call
        and parses the returned text
        """
    item = jsonable_encoder(item)
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string)
    ingredients = parse_ingredients(texts[0].description)
    return ingredients


@all_routes.route("/recipe_parser/instructions/")
def instructions(item: ImageJson):
    """
        takes in a Json, decodes the string in it to a picture, makes a vision api call
        and parses the returned text
        """
    item = jsonable_encoder(item)
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string)
    instructions = parse_instructions(texts[0].description)
    return instructions


@all_routes.route("/ingredients/getter")
def feature(item: StringJson):
    """
        Queries data base from a given name of a recipe, returns ingredients of recipes
        with matching title where the ingredients occur in more than 25 % of recipes.
        """
    item = jsonable_encoder(item)
    word_string = item['word']
    results_json = ingredient_getter(word_string)
    return results_json
