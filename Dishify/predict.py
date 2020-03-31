from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


def image_parse(uri):
    '''
    Makes a call to Google Vision's OCR API and parses all identifiable text from an image file.
    :param uri: Takes in URI object where image file is located.
    :return: Returns blocks of text obtained from the Google Vision API.
    '''

    # Vision API call using URI
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.document_text_detection(image=image)

    recipe_blocks = len(response.full_text_annotation.pages[0].blocks)
    recipe_texts = []

    for block in response.full_text_annotation.pages[0].blocks:

        blocktext = []

        for paragraph in block.paragraphs:

            for word in paragraph.words:

                wordtext = ''
                for symbol in word.symbols:
                    wordtext += symbol.text

                blocktext.append(wordtext)

        recipe_texts.append(blocktext)

    recipe_dict = {'blocks': recipe_blocks, 'texts': recipe_texts}

    # return data
    return recipe_dict