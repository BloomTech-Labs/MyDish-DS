import predict
import processing
import json

#uri = 'https://images-na.ssl-images-amazon.com/images/I/81%2B1uNsyR0L.jpg'
uri = 'https://cdn.shopify.com/s/files/1/1133/5284/products/9781771644761_002_iart.jpg'

response = predict.image_parse(uri)

texts = response.text_annotations
recipe = str(texts[0].description)

response = processing.main_function(recipe)

app_json = json.dumps(response)
print(response)
