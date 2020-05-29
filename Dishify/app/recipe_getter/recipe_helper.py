from recipe_parser.helper import improve_fractions, is_number
from text_to_num import alpha2digit
import re


def parse_ingredients_mod(scraper):

    """
    
    """

    ingredients = scraper.ingredients()

    ingredients = "\n".join(ingredients)

    ingredients = improve_fractions(ingredients)

    # remove all special characters
    ingredients = re.sub('[^A-Za-z0-9 ,;.:-?/!""\n]+', '', ingredients)

    # since all websites that can be accessed by the recipe_scraper library
    # are in english there is no need to detect the language
    ingredients = [alpha2digit(line, "en").split() for line in ingredients.splitlines()]

    # list to store ingredients
    all_ingredients = []

    # parse each line of the recipe for unit, quantity and ingredient
    for line in ingredients:
        
        length = len(line)
        
        if length == 1:
            
            # either this line is part of the previous line or it is an ingredient 
            # that needs no unit or qantity. This code will treat it as an ingredient. 
            # Web will hopefully implement functionality that enables the user to 
            # add this line to the previous ingredient if necessary.
            
            all_ingredients.append({"quantity":None, "unit":None, "ingredient":line[0]})
            continue
            
        elif length == 2:
            
            # this line is most probably an ingredient and a quantity 
            
            if (is_number(line[0][0]) and not is_number(line[1][0])):
            
                all_ingredients.append({"quantity":line[0], "unit":None, "ingredient":line[1]})
                continue
            
            elif (not is_number(line[0][0]) and is_number(line[1][0])):
                
                all_ingredients.append({"quantity":line[1], "unit":None, "ingredient":line[0]})
                continue
            
            else:
                
                # the last case covers both the possibility that both strings contain 
                # a number or that both dont. For both cases the same treatment makes sense.
                # 1. If they both contain numbers something went wrong and saving this line 
                # only under ingredient will make it easier for the user to modify it.
                # 2. If they both dont contain numbers they are probably part of the previous 
                # line and probably part of the ingredient part of that line. Saving
                # this as one string under ingredient will make it easier for the user 
                # to modify this part.  
                all_ingredients.append({"quantity":None, "unit":None, "ingredient":" ".join(line)})
                continue
                
        elif length > 2:
            
            number_map = [1 if is_number(word) else 0 for word in line]
            
            instances_number = sum(number_map)
                          
            if instances_number ==  0:

                # in the line there are no words that begin with a number
                
                all_ingredients.append({"quantity":None, "unit":None, "ingredient":" ".join(line)})
                continue
                
                              
            elif instances_number == 1:
                
                # in the line there is one word that begins with a number
                
                index = number_map.index(1)
                
                if index == 0:
                    
                    all_ingredients.append({"quantity":line[0], "unit":line[1], "ingredient":" ".join(line[2:])})
                    continue
                    
                elif index == 1:
                    
                    all_ingredients.append({"quantity":line[1], "unit":line[0], "ingredient":" ".join(line[2:])})
                    continue
                      
                elif index == (length - 2):
                    
                    all_ingredients.append({"quantity":line[-2], "unit":line[-1], "ingredient":" ".join(line[:-2])})
                    continue
                         
                elif index == (length -1):
                    
                    all_ingredients.append({"quantity":line[-1], "unit":line[-2], "ingredient":" ".join(line[:-2])})
                    continue
                    
                else:
                    
                    all_ingredients.append({"quantity":None, "unit":None, "ingredient":" ".join(line)})
                    continue
                           
            else:
                
                # in the line there are two or more words that begin with a number

                if instances_number == 2 and (number_map[0] + number_map[1] == 2) and length > 3:

                    all_ingredients.append({"quantity": " ".join(line[:2]), "unit":line[2], "ingredient":" ".join(line[3:])})
                    continue

                else:
                    all_ingredients.append({"quantity":None, "unit":None, "ingredient":" ".join(line)})
                    continue
                    
    ingredients_dict = {"ingredients": all_ingredients}

    return ingredients_dict   










