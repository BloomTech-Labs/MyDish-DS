from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from recipe_parser.helper import decode_string_and_api_call
from recipe_parser.ingredients import parse_ingredients
from recipe_parser.instructions import parse_instructions
from ingredients_populater.getter import ingredient_getter
import json


class ImageJson(BaseModel):
    image: str

class StringJson(BaseModel):
    word: str

application = app = FastAPI()


@app.post("/recipe_parser/ingredients/")
async def create_item(item: ImageJson):
    
    """
    takes in a Json, decodes the string in it to a picture, makes a vision api call,
    parses the returned text, and returns a json
    """

    item = jsonable_encoder(item)
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string)
    if len(texts) == 0:
        return json.dumps({"error":"The image does not contain text"})
    else:
        ingredients_dict_json = parse_ingredients(texts[0].description)
        return ingredients_dict_json



@app.post("/recipe_parser/instructions/")
async def create_item(item: ImageJson):

    """
    takes in a Json, decodes the string in it to a picture, makes a vision api call,
    parses the returned text, and returns a json
    """

    item = jsonable_encoder(item)
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string)
    if len(texts) == 0:
        return json.dumps({"error":"The image does not contain text"})
    else:
        instructions_dict_json = parse_instructions(texts[0].description)
        return instructions_dict_json


@app.post("/ingredients/getter")
async def feature(item: StringJson):

    """
    #Queries data base from a given name of a recipe, returns ingredients of recipes
    #with matching title where the ingredients occur in more than 25 % of recipes. 
    """

    item = jsonable_encoder(item)
    word_string = item['word']
    results_json = ingredient_getter(word_string)
    return results_json

