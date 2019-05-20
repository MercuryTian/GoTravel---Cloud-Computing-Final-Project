import json
import boto3
from user_parse import parse

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    userID = event['userId']
    
    try:
        user = dynamodb_client.get_item(
            TableName='gotravel-users',
            Key={
                'userID': {
                    'S': userID
                }
            },
        )['Item']
    except:
        user = {}

    user_parsed = parse(user)
    
    '''
    return {
        'statusCode': 200,
        'body': user_parsed
    }
    '''
    return user_parsed
