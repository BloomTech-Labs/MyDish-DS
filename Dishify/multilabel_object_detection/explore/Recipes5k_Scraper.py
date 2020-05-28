import urllib
from bs4 import BeautifulSoup, NavigableString

'''
Web scraping script for Recipes5k
'''


def getIngredientsFromFile():
    fp = open("ingredients_Recipes5k.txt", "r")
    words = [word.strip() for line in fp.readlines()
             for word in line.split(',') if word.strip()]
    fp.close()
    return words


def cleanIngredientsv1():
    ingredients = getIngredientsFromFile()
    dictIngredients = {}
    for ingredient in ingredients:
        try:
            dictIngredients[ingredient].append(ingredient)
        except:
            dictIngredients[ingredient] = [ingredient]

    print(dictIngredients.keys())


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
baseURL = 'http://www.bbc.co.uk/food/ingredients/by/letter/'
ingre = []


def downloadIngredients():
    for letter in alphabet:
        url = baseURL + letter
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)

        ingredients = soup.findAll("li", {"class": "resource food"})
        for elem in ingredients:
            word = ' '.join((elem.find('a').contents)
                            [-1].replace('\n', '').split())
            word = unicodedata.normalize('NFKD', word).encode(
                'ascii', 'ignore').lower()
            ingre.append(word)

        time.sleep(0.5)

    fp = open('baseIngredients.txt', 'w')
    fp.write(','.join(ingre))
    fp.close()
