from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from recipe_parser.helper import google_api_call
from recipe_parser.ingredients import parse_ingredients
from recipe_parser.instructions import parse_instructions
from ingredients_populater.getter import ingredient_getter
import json
import os


class StringJson(BaseModel):
    word: str

application = app = FastAPI()


@app.post("/recipe_parser/ingredients")
async def create_upload_file(file: UploadFile = File(...)):

    """
    accepts a JPEG,  makes a vision api call,
    parses the returned text, and returns a json
    """
    image = file.file
    texts, blocks = google_api_call(image)

    if len(texts) == 0:
        return json.dumps({"error":"The image does not contain text"})
    else:
        ingredients_dict_json = parse_ingredients(texts)
        return ingredients_dict_json



@app.post("/recipe_parser/instructions")
async def create_upload_file(file: UploadFile = File(...)):

    """
    accepts a JPEG,  makes a vision api call,
    parses the returned text, and returns a json
    """
    image = file.file
    texts, blocks = google_api_call(image)

    if len(texts) == 0:
        return json.dumps({"error":"The image does not contain text"})
    else:
        instructions_dict_json = parse_instructions(texts, blocks)
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

