import predict
import json

def lambda_handler(event, context):

    recipe = json.dumps(predict.image_parse(event['imageURL']))

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': recipe
    }

    context.succeed("done");
