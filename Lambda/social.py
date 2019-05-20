import json
import boto3
from user_parse import parse

dynamodb_client = boto3.client('dynamodb')

def get_parsed_user(userID):
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
    
    return parse(user)

def get_result(user, result, feature):
    for x in user[feature]:
        tmp = get_parsed_user(x)
        # del tmp[feature]
        # del tmp[feature]
        result[feature].append(tmp)

def lambda_handler(event, context):
    userID = event['userId']
    user = get_parsed_user(userID)

    result = {}
    result['following'] = []
    result['followers'] = []
    get_result(user, result, 'followers')
    get_result(user, result, 'following')

    '''
    return {
        'statusCode': 200,
        'body': result
    }
    '''
    return result
