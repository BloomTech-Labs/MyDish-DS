from collections import Counter
import ast
import json
import psycopg2

def string_to_list(x):
    return ast.literal_eval(x)

def ingredient_getter(word: str):
    results_dict = {}
    split_words = word.split()
    
    conn = psycopg2.connect(database ='postgres', user = 'postgres', password = 'tz6MTgxObUZ62MNv0xgp', host = 'mydishdb-dev.c3und8sjo4p2.us-east-2.rds.amazonaws.com', port = '5432')
    cursor = conn.cursor()

    command = f"SELECT * FROM recipes WHERE name ILIKE '%{split_words[0]}%' "
    if len(split_words) > 1:
        for i in range(1, len(split_words)):
            command += f"AND name ILIKE '%{split_words[i]}%' "
    command += ";"

    cursor.execute(command)
    recipe_table = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Initialize a Counter for tabulating how often each ingredient occurs
    ingredient_counts = Counter()

    # Count each instance of each ingredient
    for i in range(len(recipe_table)):
        for j in range(2, len(recipe_table[i])):
            if recipe_table[i][j]:
                ingredient = string_to_list(recipe_table[i][j])[2]
                ingredient_counts.update({ingredient: 1})
    
    # Get the top 30 ingredients sorted by most common
    top_30 = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)[:30]

    # Get the ingredients that occured in at least 25% of recipes returned
    above_25_percent = [(tup[0], round(100*tup[1]/len(recipe_table), 1)) for tup in top_30 if 100*tup[1]/len(recipe_table) >= 25]

    # Get the ingredient information and put it in a dictionary
    for item in above_25_percent:
        quantity_list = []
        unit_list = []
        for i in range(len(recipe_table)):
            for j in range(2, len(recipe_table[i])):
                if recipe_table[i][j]:
                    if string_to_list(recipe_table[i][j])[2] == item[0]:
                        quantity = string_to_list(recipe_table[i][j])[0]
                        unit = string_to_list(recipe_table[i][j])[1]

                        quantity_list.append(quantity)
                        unit_list.append(unit)

        # Getting and saving the most common quantity and unit for each ingredient
        data = Counter(quantity_list)
        quantity = data.most_common(1)
        data = Counter(unit_list)
        unit = data.most_common(1)

        results_dict[item[1]] = {'quantity': quantity[0][0], 
                            'unit': unit[0][0], 
                            'ingredient': item[0]}

    results_json = json.dumps(results_dict)
    
    return results_json
