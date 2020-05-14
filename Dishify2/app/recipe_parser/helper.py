from text_to_num import alpha2digit
import base64
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import json


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Key.json"


fractions = ['½','⅓','⅔','¼','¾','⅕','⅖','⅗','⅘','⅙','⅚',
            '⅐','⅛','⅜','⅝','⅞','⅑','⅒']

fractions_better = ['1/2','1/3','2/3','1/4','3/4','1/5','2/5','3/5','4/5',
                    '1/6','5/6','1/7','1/8','3/8','5/8','7/8','1/9','1/10']            


def improve_fractions(recipe):

    """
    function to transform from - for example - '½' to '1/2'. Makes the recipe entries 
    easier to edit for the user and enables parsing of fractions. 
    """
    for i in range(len(fractions)):
        recipe = recipe.replace(fractions[i], fractions_better[i])
        return recipe



def is_number(n):

    """
    function to check if  the first character of a string is a number. This 
    function only checks the first character to cover cases like "3-4" or "3/4". 
    """
    if len(n) == 0:
        return False
    
    try:
        float(n[0])  
        
    except ValueError:
        return False
    return True


def text_to_number(recipe):

    """
    function to transform written numbers in a string ("one hundred horses") to 
    their integer form ("100 horses"). Works for English, Spanish and French. 
    It takes advantage of the fact that the Google Vision API recognises 
    the language of the text in the picture that was taken.
    """    
    if texts[0].locale == "en":
        
        recipe = alpha2digit(recipe, "en")
        return recipe
    
    elif texts[0].locale == "es":
        
        recipe = alpha2digit(recipe, "es")
        return recipe
        
    elif texts[0].locale == "fr":
        
        recipe = alpha2digit(recipe, "fr")
        return recipe
    
    else:
        return recipe



def decode_string_and_api_call(image_string):

    """
    function to decode the base64 decoded string and make a google vision api 
    call with the picture.
    """
    # decode image_string
    decoded_string = base64.b64decode(image_string)

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Perform text detection
    image = types.Image(content=decoded_string)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations
    blocks = response.full_text_annotation

    return texts, blocks


def clean_recipe(recipe):

    """
    function to clean string to improve parsing
    """
    
    recipe = improve_fractions(recipe)

    # remove all special characters
    recipe = re.sub('[^A-Za-z0-9 ,;.:-?!""\n]+', '', recipe)

    # apply the text2num library if the recipe is in French, Spanish or English. 
    # This will transform written numbers (like "one hundred") to 
    # integers in string format (like "100"). If the time permits a german 
    # version of this library will be implemented.
    recipe = text_to_number(recipe)
    
    return recipe
    
def find_order(recipe):

    """
    function to find an order in a string that contains instructions
    in the form of: 
    "these are my instructions: 1. chop onions 2. fry onions 
    3. eat onions 4. digest onion"

    will be transformed to 

    {'instructions': [{'steps': 'these are my instructions: '},
    {'steps': '1. chop onions '},
    {'steps': '2. fry onions '},
    {'steps': '3. eat onions '},
    {'steps': '4. digest onion'}]}

    """
    
    nums = []
    
    steps = []
    
    for i in range(len(recipe)):
        
        if recipe[i].isnumeric():
            
            nums.append([i, recipe[i]])
            
    print(nums)
            
    # check if first number in string is 1
    if nums[0][1] == "1":
             
        index_order = [0]
        
        counter = 2
        
        for i in range(1,len(nums)):
        
            # check if there are at least 10 characters between 
            # assumed instances of structure in the string.
            if nums[i][1] == str(counter): 
                
                if (nums[i][0] - nums[index_order[-1]][0]) > 10:
                    
                    index_order.append(i)
                    
                    counter = counter + 1
            
        # check if there is at least a succesion of 1, 2, 3 in the string. 
        # If that is the case the assumption is that the string is structured. 
        if len(index_order) > 2:
            
            # check if string started with "1"
            if nums[0][0] > 1:
            
                steps.append({"steps": recipe[:nums[0][0]]})
                
                # iterate over index_order except the last element since it needs 
                # to be treated differently
                for i in range(len(index_order) -1):
                    
                    steps.append({"steps": recipe[nums[index_order[i]][0]:nums[index_order[i+1]][0]]})
                    
                # append the last step 
                steps.append({"steps": recipe[nums[index_order[-1]][0]:]})
            
                return {"instructions":steps}
            
        else:
            
            return {"instructions": recipe}
                    
    else:
        
        return {"instructions": recipe}









