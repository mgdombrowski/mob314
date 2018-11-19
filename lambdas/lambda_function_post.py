import base64
import json
import uuid
import datetime
import os
import boto3

print('Loading function')
kinesisclient = boto3.client('kinesis', region_name='us-east-1')
client = boto3.client('comprehend')
pinpointclient = boto3.client('pinpoint')


def lambda_handler(event, context):
    '''Respond to Facebook page event webhook with challenge
    '''
    print("Received event: " + str(event))
    app_id = os.environ['PinpointAppId']
    body = json.loads(event['body'])
    userId = body['entry'][0]['changes'][0]['value']['from']['name'].replace(" ", "")
    post_content = body['entry'][0]['changes'][0]['value']['message']
    
    response = kinesisclient.put_record(
                StreamName='page_updates',
                Data=event['body'],
                PartitionKey=str(uuid.uuid4())
    )

    try: 
        pinpointclient.get_endpoint(ApplicationId=app_id, EndpointId=userId)
    except Exception as e:
        print("Error occurred: ", e)
    else:
        # if endpoint exists, do sentiment analysis, send push, update endpoint
        response = client.detect_sentiment(
            Text=post_content,
            LanguageCode='en'
        )
        print(response)
        
        if response['Sentiment'] == 'NEUTRAL':
            pinpointresponse = pinpointclient.send_messages(
                ApplicationId=app_id,
                MessageRequest={
                    'Endpoints': {
                        userId: {}
                    },
                    'MessageConfiguration': {
                        'GCMMessage': {
                            'Action': 'OPEN_APP',
                            'Body': 'Thanks for the feedback! Fill out this 2-question survey and get free gear https://tinyurl.com/SomeSurveyURL',
                            'Title': 'Thank you very much!'
                        }
                    }
                }
            )
            print(pinpointresponse)
            endpointresponse = pinpointclient.update_endpoint(
                ApplicationId=app_id,
                EndpointId=userId,
                EndpointRequest={
                    'EffectiveDate': datetime.datetime.now().isoformat(),
                    'RequestId': str(uuid.uuid4()),
                    'User': {
                        'UserAttributes': {
                            'Sentiment': [
                                'Neutral',
                            ]
                        }
                    }
                }
            )
            print(endpointresponse)
