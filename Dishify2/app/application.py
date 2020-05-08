from fastapi import FastAPI
from pydantic import BaseModel
from recipe_parser.helper import decode_string_and_api_call
from recipe_parser.ingredients import parse_ingredients
from recipe_parser.instructions import parse_instructions



class Item(BaseModel):
    image: str

application = app = FastAPI()



@app.post("/recipe_parser/ingredients/")
async def create_item(item: Item):
    
    """

    """
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string) 
    ingredients = parse_ingredients(texts[0].description)
    return ingredients



@app.post("/recipe_parser/instructions/")
async def create_item(item: Item):

    """
    
    """
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string) 
    instructions = parse_instructions(texts[0].description)
    return instructions

