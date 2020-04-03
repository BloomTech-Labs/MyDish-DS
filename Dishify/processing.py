# import predict
import string
import re

# recipe = """
# Buffalo Cauliflower Bites
# There's nothing like settling into a plate of spicy, tangy wings while watching a
# game. But let's be honest—the sauce is usually better than the chicken! In my
# Plant Paradox-approved version, you can still enjoy the addictive flavor and
# crunch of your favorite game day treat-without the halftime stomachache!
# SERVES 4 TO 6
# 1. Preheat the oven to 450°F.
# FOR THE BUFFALO SAUCE
# 1 cup Frank's Red Hot Sauce
# 2 teaspoons avocado oil
# or ghee
#  1tablespoon coconut aminos
# 1 teaspoon apple cider vinegar
# 2. First, make the buffalo sauce: combine the hot sauce,
# avocado oil or ghee, coconut aminos, and apple cider
# vinegarin a glass jar with a lid and shake well. Refrigerate
# until needed.
# 3. Drizzle a baking sheet liberally with olive oil, or line
# with parchment. Set aside.
# 1 medium head of cauliflower,
# chopped
# 2 tablespoons extra-virgin
# olive oil, plus more for
# baking sheet
# 2 tablespoons cassava flour
# 1 teaspoon iodized sea salt
# 1 teaspoon ground black
# pepper
# 2 teaspoons garlic powder
# cup buffalo sauce (recipe
# above)
# Plain coconut yogurt, for
# dipping
# 4. Toss the cauliflower, olive oil, cassava flour, and spices
# together in a large bowl until cauliflower is evenly
# coated.
# 5. Transfer to a baking sheet and bake for 30 minutes,
# turning every 10 minutes so the cauliflower crisps on
# all sides.
# 6. Brush with the buffalo sauce, then bake an additional
# 10 minutes.
# 7. Serve with yogurt and any extra buffalo sauce for dip-
# ping.
# APPETIZERS AND SNACKS
# 91
# """

measurementUnits = ['teaspoons', 'tablespoons', 'cups', 'containers', 'packets', 'bags', 'quarts', 'pounds', 'cans',
                    'bottles',
                    'pints', 'packages', 'ounces', 'jars', 'heads', 'gallons', 'drops', 'envelopes', 'bars', 'boxes',
                    'pinches',
                    'dashes', 'bunches', 'layers', 'slices', 'links', 'bulbs', 'stalks', 'squares', 'sprigs',
                    'fillets', 'pieces', 'legs', 'thighs', 'cubes', 'granules', 'strips', 'trays', 'leaves', 'loaves',
                    'halves']

quantities = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
              '1', '2', '3', '4', '5', '6', '7', '8', '9']

ingredients = ['aminos', 'sea', 'buttermilk', 'cottage', 'cream', 'creamer', 'creamy', 'creme', 'ghee', 'half-and-half',
               'milk', 'yogurt', 'bocconcini', 'mozzarella', 'gouda', 'swiss', 'brie', 'bacon', 'beefs', 'burgers',
               'chorizo', 'dogs', 'frankfurters', 'giblets', 'ham', 'lambs', 'livers',
               'meatballs', 'meatloaves', 'meats', 'mignon', 'mincemeat', 'pepperonis', "pig's", 'porks',
               'prosciutto', 'ribs', 'roasts', 'sausages', 'sirloin', 'tripe', 'veal', 'venison', 'kielbasas',
               'liverwurst', 'wieners', 'cotechino', 'linguica', 'pastrami', 'squirrels', 'sauerbraten',
               'picadillo', 'carcass', 'brains', 'mortadella', 'rounds', 'sweetbread', 'toad', 'tinga',
               'embutido', 'hash', 'broil', 'brisket', 'franks', 'pigs', 'rouladen', 'chops', 'scrapple',
               'barbeque', 'spareribs', 'bologna', 'bratwursts', 'chickens', 'ducks', 'goose', 'hens', 'pollo',
               'salami', 'turkey',
               'pheasant', 'quail', 'turducken', 'drumettes', 'wings', 'roosters', 'albacores', 'bass', 'catfish',
               'cods', 'fish', 'flounder', 'grouper', 'haddock', 'halibut', 'mahi',
               'monkfish', 'salmon', 'shark', 'snapper', 'sole', 'swordfishes', 'trouts', 'tunas', 'bluefish',
               'bonito', 'rockfish', 'mackerel', 'naruto', 'drum', 'marlin', 'tilapia', 'carp', 'kingfish',
               'mullets', 'whitefish', 'kippers', 'torsk', 'saltfish', 'anchovies', 'calamaris', 'clams', 'crabs',
               'crabmeat', 'crawfish', 'lobsters', 'mussels',
               'oysters', 'prawns', 'scallops', 'seafood', 'shrimps', 'squids', 'snails', 'shellfish', 'caviar',
               'beans', 'chickpeas', 'nuts', 'seeds', 'tofu', 'whey', 'buckwheat', 'protein', 'soybeans',
               'soy', 'tempeh', 'lentils', 'masoor', 'gluten', 'pine', 'falafel', 'portobello', 'apples', 'apricots',
               'bananas', 'blackberries', 'blueberries', 'cantaloupe', 'cherries', 'citrons',
               'citrus', 'coconuts', 'cranberries', 'currants', 'elderberries', 'figs', 'fruitcakes', 'fruits',
               'gooseberries', 'grapefruit', 'grapes', 'guava', 'honeydew', 'huckleberries', 'kiwis', 'kumquats',
               'lemonade', 'lemons', 'limes', 'mangoes', 'marrons', 'mincemeat', 'mulberries', 'nectarines', 'oranges',
               'papayas', 'peaches', 'pears', 'persimmon', 'persimmons', 'pineapples', 'plums', 'prunes', 'raisins',
               'raspberries', 'slushies', 'smoothies', 'sorrel', 'strawberries', 'tangerines', 'watermelons', 'yuzu',
               'lingonberries', 'plantains', 'juniper', 'lingonberries', 'pomegranates', 'serviceberries',
               'zinfandel', 'lychees', 'carambola', 'uvas', 'artichokes', 'arugula', 'asparagus', 'avocados', 'bamboo',
               'beets', 'broccoli', 'cabbage',
               'calzones', 'carrots', 'cauliflower', 'celery', 'chilis', 'chives', 'choy', 'cilantro', 'coleslaw',
               'coriander', 'cucumber', 'cucumbers', 'dates', 'eggplant', 'eggplants', 'endive', 'escarole',
               'galangal', 'haystacks', 'jicama', 'kale', 'kohlrabi', 'kucai', 'leeks', 'lettuce',
               'mushrooms', 'okra', 'olives', 'onions', 'parsley', 'parsnips', 'peas', 'peppers', 'pickles',
               'pizzas', 'potatoes', 'pumpkins', 'radishes', 'rutabagas', 'salad', 'sauerkraut', 'shallots', 'slaws',
               'spinach', 'sprouts', 'squash', 'tamarind', 'taros', 'tomatillo', 'tomatillos', 'tomatoes', 'turnips',
               'vegetable', 'vegetables', 'veggies', 'watercress', 'yams', 'zucchinis', 'chervil', 'daikon', 'iceberg',
               'nopales', 'pimentos', 'radicchio', 'karengo', 'nori', 'succotash', 'truffle', 'chard', 'fries',
               'leaves',
               'browns', 'romain', 'palm', 'sorghum', 'aloo', 'haricots', 'caprese', 'salata', 'shiitake', 'Jell-O®',
               'butterscotch', 'candied', 'candy', 'caramels', 'frosting', 'fructose', 'gingersnaps',
               'glaces', 'glaze', 'glycerin', 'glycerol', 'gumdrops', 'gummi', 'honey', 'icing', 'jellybeans',
               'ladyfingers', 'licorice', 'macaroons', 'maple', 'marrons glaces', 'marshmallows', 'marzipan',
               'molasses', 'pastries', 'pectin', 'peppermints', 'pie', 'piping', 'puddings', 'puff', 'sourball',
               'sprinkles', 'sucanat', 'sugar', 'sweetener', 'syrup', 'tarts', 'toffee', 'twinkies', 'colaciones'
                                                                                                     'sherbet',
               "hershey®'s", 'candies', "confectioners'", 'fudge', 'taffy', 'pink', 'sherbet', 'alfredo', 'applesauce',
               'chutney', 'cannoli', 'dips', 'guacamole', 'hummus', 'paste', 'spreads',
               'tahini', 'tzatziki', 'denjang', 'salsa', 'sauce', 'tapenade', 'coating', 'teriyaki',
               'aioli', 'checca', 'amatriciana', 'ragu', 'marinara', 'dressing', 'jam', 'ketchup', 'marinade',
               'marjoram', 'mayonnaise', 'mirin', 'mustard',
               'pesto', 'relish', 'shoyu', 'tamari', 'vinaigrette', 'gochujang', 'broth', 'chowder', 'dashi', 'soup',
               'stew', 'jambalaya', 'gumbo', 'gazpacho', 'goulash', 'pho',
               'slumgullion', 'cioppino', 'minestrone', 'almonds', 'butternuts', 'candlenuts', 'cashews', 'chestnuts',
               'hazelnuts', 'macadamia', 'nuts',
               'peanuts', 'pecans', 'pistachios', 'walnuts', 'nuts', 'anisette', 'beer', 'bitters', 'bourbon', 'brandy',
               'cacao', 'chambord', 'champagne',
               'cognac', 'eggnog', 'kirsch', 'kirschwasser', 'liqueur', 'rum', 'schnapps', 'sherry', 'ale',
               'spritz', 'tequila', 'vermouth', 'vodka', 'whiskey', 'wine', 'campari', 'alcohol', 'absinthe',
               'cachaca', 'liquor', 'cointreau', 'curacao', 'sake', 'sec', 'calvados', 'galliano', 'lillet',
               'margaritas', 'coladas', 'negroni', 'mojitos', 'mimosas', 'bahama', 'slammer', 'sauvignon', 'chablis',
               'martinis', 'tequinis', 'spritzs', 'cosmopolitan', 'hurricanes', 'sangria', 'sex', "shaggy's", 'nipples',
               'stoli', 'allspice', 'anise', 'arrowroot', 'basil', 'bay', 'capers', 'caraway', 'cardamom', 'cassava',
               'cayenne', 'chocolate', 'cilantro', 'cinnamon', 'cloves', 'cocoa', 'coriander', 'cumin', 'dill',
               'fennel', 'flax', 'garlic', 'ginger', 'herbs', 'kalonji', 'mace', 'masala', 'miso', 'monosodium',
               'nutmeg', 'oregano', 'paprika', 'pepper', 'peppercorns', 'pimento', 'poppy', 'poppyseed',
               'powder', 'rhubarb', 'rosemary', 'saffron', 'sage', 'salt', 'savory', 'seasoning', 'sesame', 'spices',
               'sunflower', 'tarragon', 'thyme', 'turmeric', 'vanilla', 'watercress', 'spearmint', 'comfort',
               'angelica', 'dijon', 'horseradish', 'jerk', 'wasabi', 'spicy', 'jalapenos', 'pepperoncinis', 'chiles',
               'bagels', 'baguettes', 'barley', 'biscuits', 'bran', 'bread', 'buns', 'cereal', 'corn', 'cornbread',
               'cornstarch', 'couscous', 'crackers', 'croutons', 'crusts', 'dough', 'granola', 'hominy', 'kasha',
               'masa', 'matzo', 'millet', 'muffins', 'oats', 'pitas', 'popcorn', 'pretzels', 'quinoa', 'rice', 'rolls',
               'shortbread', 'sourdough', 'stuffing', 'tapioca', 'toasts', 'tortillas', 'wheat', 'kaiser', 'cornmeal',
               'breadcrumbs', 'graham', 'bulgur', 'farina', 'oatmeal', 'croissants', 'polenta', 'grits', 'pumpernickel',
               'sago', 'seitan', 'grains', 'taters', 'risotto', 'shells', 'amarettini', 'mochi', 'cornflakes', 'pilaf',
               'puppies', 'farfalle', 'fettuccine', 'lasagnas', 'linguine', 'mac', 'macaroni', 'manicotti', 'noodles',
               'pasta',
               'farfel', 'vermicelli', 'tagliatelle', 'cannelloni', 'penne', 'burritos', 'calzones', 'dumplings',
               'empanadas', 'fajitas', 'hero', 'pie', 'pinwheels', 'pizzas',
               'quesadillas', 'sandwiches', 'tacos', 'tourtiere', 'wontons', 'hoagie', 'pierogies', 'rarebit',
               'joes', 'enchiladas', 'pierogi', 'bierrocks', 'torta', 'reuben', 'wraps', 'piroshki', 'tamales',
               'bruschetta', 'antipasto', 'hamburger', 'muffuletta', 'blanket', 'runzas', 'samosas', 'sambousas',
               'chalupas', 'spanakopita', 'submarine', 'casseroles', 'curry', 'lasagna', 'marzetti', 'mostaccioli',
               'spaghetti', 'stroganoff', 'ziti',
               'pastini', 'pastitsio', 'fideo', 'spaghettini', 'moussaka', 'tortellinis', 'tallerine', 'talerine',
               'scampi', 'ravioli', 'pad', 'gnocchi', 'spaetzle', 'stromboli', 'tabbouleh', 'kabobs', 'suey',
               'frittatas', 'quiches', 'raita', 'shieldzini', 'stir',
               'sukiyaki', 'beverage', 'cider', 'coffee', 'dew™', 'drink', 'eggnog', 'epazote', 'espresso', 'gin',
               'juices',
               'lemonade', 'limeade', 'milk', 'rosewater', 'soda', 'tea', 'wassail', 'punch', 'shake', 'shirley',
               'americano', 'oil', 'vinegar', 'water', 'snow', 'ice', 'ammonia', 'baking', 'eggs', 'flour', 'margarine',
               'yeast', 'bisquick®', 'butter', 'gelatin', 'gravy', 'lard', 'lecithin', 'ovalette', 'shortening',
               'xanthan', 'suet', 'carnations', 'coloring', 'dust', 'flowers', 'lilies', 'spray', 'toppings',
               'drippings', 'powdered',
               'gold', 'sticks', 'skewers', 'toothpicks', 'glue', 'jars', 'extract', 'flavorings', 'mint', 'pandan',
               'hickory', 'flavored', 'mesquite', 'wood',
               'hardwood', 'food', 'mixes']


def plural_checker(string, plural_string):
    # only check plurals if first 3 letters match
    if string[0] != plural_string[0]:
        return None

    if len(string) > 1 and len(plural_string) > 1 and string[1] != plural_string[1]:
        return None

    if len(string) > 2 and len(plural_string) > 2 and string[2] != plural_string[2]:
        return None

    # check all possible plurals of string
    if string == plural_string or \
            string + "s" == plural_string or \
            string + "es" == plural_string or \
            string[:-1] + "ies" == plural_string or \
            string[:-1] + "ves" == plural_string:
        return plural_string

    return None


def checking_plurals(string, plural_list):
    for plural_string in plural_list:
        if plural_checker(string, plural_string):
            return plural_string

    return None


def match_and_split(matches, recipe):
    split_matches = []
    i = 0
    match_locations = []

    for match in matches:

        match_locations.append(match.start())

        if i == 0 or ((match_locations[i]) - (match_locations[i - 1])) >= 100:
            pass
        else:
            split_matches.append(str(recipe[match_locations[i - 1]:match_locations[i]]))

        i += 1

    return split_matches


def cleaner(split_matches):
    clean_matches = []

    for match in split_matches:
        cleaner_match = match.translate(str.maketrans('', '', string.punctuation))

        clean_matches.append(cleaner_match)

    return clean_matches


def measurement_filter(split_matches):
    """
    check if each string inside the split matches is inside the plural list for measurements. if it's true,
    add to curated strings, if it's not do nothing. return curated strings
    """
    curated_matches = []

    for match in split_matches:
        for string in match.split():
            if checking_plurals(string, measurementUnits):
                curated_matches.append(match)
                break

    return curated_matches


def ingredient_sorter(curated_matches):
    '''
    With each match, grab the quantity, unit and ingredient and add each one to a separate list.
    :param curated_matches:
    :return: ingredient dictionary
    '''

    final_ingredients = []

    for match in curated_matches:
        full_ing = {}
        full_ing_name = []
        for word in match.split():

            if word in quantities:
                full_ing["quantity"] = word

            if checking_plurals(word, measurementUnits):
                full_ing["units"] = word

            if checking_plurals(word, ingredients):
                full_ing_name.append(word)

            if word == 'or':
                full_ing_name.append(word)

        full_ing_text = ' '.join(word for word in full_ing_name)

        full_ing["name"] = full_ing_text

        final_ingredients.append(full_ing)

    # clean_name = []
    # for word in match.split():
    # 	if word in quantities:
    # 		clean_name.append(word)

    return final_ingredients


def final_check(matches):
    for match in matches:
        for ing_names in matches:
            if len(ing_names) > 4:
                match.remove(ing_names)

    return matches


# def instruction_getter(recipe):
#     pattern = re.compile(r'')
#     matches = pattern.finditer(recipe)
#
#     return matches

def main_function(recipe):

    pattern = re.compile(r'[0-9]+')

    matches = pattern.finditer(recipe)

    split_matches = match_and_split(matches, recipe)

    split_matches = cleaner(split_matches)

    curate_matches = measurement_filter(split_matches)

    unmastered_final = ingredient_sorter(curate_matches)

    final = final_check(unmastered_final)

    instructions = ["""
    1. Preheat the oven to 450°F.
    2. First, make the buffalo sauce: combine the hot sauce,
    avocado oil or ghee, coconut aminos, and apple cider
    vinegar in a glass jar with a lid and shake well. Refrigerate
    until needed.
    3. Drizzle a baking sheet liberally with olive oil, or line
    with parchment. Set aside.
    4. Toss the cauliflower, olive oil, cassava flour, and spices
    together in a large bowl until cauliflower is evenly
    coated.
    5. Transfer to a baking sheet and bake for 30 minutes,
    turning every 10 minutes so the cauliflower crisps on
    all sides.
    6. Brush with the buffalo sauce, then bake an additional
    10 minutes.
    7. Serve with yogurt and any extra buffalo sauce for dip-
    ping."""]

    recipe_dict = {'ingredients': final, 'instructions': instructions}
    return recipe_dict
