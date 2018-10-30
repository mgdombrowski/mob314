import boto3
import json
import os

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Respond to Facebook page event webhook with challenge
    '''
    print("Received event: " + json.dumps(event, indent=2))
    challenge = int(event['queryStringParameters']['hub.challenge'])
    verify_token = event['queryStringParameters']['hub.verify_token']

    try:
        if os.environ['verify_token'] == verify_token:
            return respond(None, challenge)
        else:
            return respond(ValueError('Token verification failed.'))
    except Exception as e:
        return respond(ValueError('Error received: "{}"'.format(e)))
