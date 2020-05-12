import re
from app.route.recipe_parser.helper import text_to_number, improve_fractions
import json


def parse_ingredients(recipe):
    """
    base dictionary
    """
    base_dict_ingr = {"quantity": None, "unit": None, "ingredient": None}

    # list to save modified base dictionaries
    ingredients = []

    improve_fractions(recipe)

    # remove all special characters
    recipe = re.sub('[^A-Za-z0-9 ,;.:-?!""\n]+', '', recipe)

    # apply the text2num library if the recipe is in French, Spanish or English.
    # This will transform written numbers (like "one hundred") to
    # integers in string format (like "100"). If the time permits a german
    # version of this library will be implemented.
    recipe = text_to_number(recipe)

    # transform the string into an iterable format, line for line, word for word.
    recipe = [line.split() for line in recipe.splitlines()]

    # parse each line of the recipe for unit, quantity and ingredient
    for line in recipe:

        length = len(line)

        if length == 1:

            # either this line is part of the previous line or it is an ingredient that needs no unit or qantity. This code will treat it as an ingredient.
            # Web will hopefully implement functionality that enables the user to add this line to the previous ingredient if necessary.

            new_entry = base_dict_ingr.copy()
            new_entry["ingredient"] = line[0]
            ingredients.append(new_entry)

        elif length == 2:

            # this line is most probably an ingredient and a quantity

            new_entry = base_dict_ingr.copy()

            if (is_number(line[0][0]) and not is_number(line[1][0])):

                new_entry["quantity"] = line[0]
                new_entry["ingredient"] = line[1]
                ingredients.append(new_entry)

            elif (not is_number(line[0][0]) and is_number(line[1][0])):

                new_entry["quantity"] = line[1]
                new_entry["ingredient"] = line[0]
                ingredients.append(new_entry)

            else:

                # the last case covers both the possibility that both strings contain a number or that both dont. For both cases the same treatment makes sense.
                # 1. If they both contain numbers something went wrong and saving this line only under ingredient will make it easier for the user to modify it.
                # 2. If they both dont contain numbers they are probably part of the previous line and probably part of the ingredient part of that line. Saving
                # this as one string under ingredient will make it easier for the user to modify this part.

                new_entry["ingredient"] = " ".join(line)
                ingredients.append(new_entry)

        elif length > 2:

            # here a if else statement needs to be added that checks if there is a "," in the string. If so the second part needs to be checked if it is
            # a seperate ingredient.

            # this line contains most probably an amount, a unit and an ingredient

            new_entry = base_dict_ingr.copy()

            for i in range(length):

                if (is_number(line[i]) and (i < (length - 1))):

                    new_entry["quantity"] = line[i]
                    new_entry["unit"] = line[i+1]

                    del line[i:i+2]
                    new_entry["ingredient"] = " ".join(line)

                    ingredients.append(new_entry)

                elif (is_number(line[i]) and (i == (length - 1))):

                    new_entry["quantity"] = line[i]

                    del line[i]
                    new_entry["ingredient"] = " ".join(line)

                    ingredients.append(new_entry)

                else:

                    new_entry["ingredient"] = " ".join(line)

                    ingredients.append(new_entry)

        else:
            continue

        ingredients_dict = {"ingredients": ingredients}
        return json.dumps(ingredients_dict)
