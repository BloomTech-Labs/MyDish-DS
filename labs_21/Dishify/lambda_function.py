import predict
import json


def lambda_handler(event, context):
    '''
    AWS Lambda function handler. Executes predict.py when API Gateway receives a request.
    :param event['imageURL']: Contains URI for image file to be parsed.
    :return: JSON containing dictionary of parsed text from image.
    '''
    recipe = json.dumps(predict.image_parse(event['imageURL']))

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': recipe
    }

    context.succeed("done")
