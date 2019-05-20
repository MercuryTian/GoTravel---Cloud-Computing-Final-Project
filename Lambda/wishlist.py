import json
import boto3

db_client = boto3.client('dynamodb')

def is_equal_location(loc1, loc2):
    if loc1['M']['latitude']['N'] == loc2['M']['latitude']['N']:
        if loc1['M']['longitude']['N'] == loc2['M']['longitude']['N']:
            return True
    return False

def if_in_wishlist(user, location):
    if 'wishlist' in user:
        for wish in user['wishlist']['L']:
            if is_equal_location(wish, location):
                return True
    return False

def lambda_handler(event, context):
    userID = event['userId']
    storyID = event['storyId']
    
    location = db_client.get_item(
        TableName='gotravel-stories',
        Key={
            'storyID': {
                'S': storyID
            }
        }
    )['Item']['location']
    
    user = db_client.get_item(
        TableName='gotravel-users',
        Key={
            'userID': {
                'S': userID
            }
        }
    )['Item']
    
    if if_in_wishlist(user, location) == False:
        db_client.update_item(
            TableName='gotravel-users',
            Key={
                'userID': {
                    'S': userID
                }
            },
            UpdateExpression='SET wishlist = list_append(if_not_exists(wishlist, :empty_list), :new_location)',
            ExpressionAttributeValues={
                ':empty_list': {'L': []},
                ':new_location': {'L': [location]}
            }
        )
        result = location
    else:
        result = 'already in wishlist'
    
    '''
    return {
        'statusCode': 200,
        'body': result
    }
    '''
