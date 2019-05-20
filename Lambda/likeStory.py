import json
import boto3

db_client = boto3.client('dynamodb')

def construct_like(time, userID):
    like = {}
    like['time'] = {'S': time}
    like['userID'] = {'S': userID}
    return like

def if_liked(userID, storyID):
    story = db_client.get_item(
        TableName='gotravel-stories',
        Key={
            'storyID': {
                'S': storyID
            }
        }
    )['Item']

    if 'likes' in story:
        for like in story['likes']['L']:
            if like['M']['userID']['S'] == userID:
                return True
    
    return False

def lambda_handler(event, context):
    time = event['time']
    userID = event['userID']
    storyID = event['storyID']

    if if_liked(userID, storyID) == False:
        like = construct_like(time, userID)
        db_client.update_item(
            TableName='gotravel-stories',
            Key={
                'storyID': {
                    'S': storyID
                }
            },
            UpdateExpression='SET likes = list_append(if_not_exists(likes, :empty_list), :new_like)',
            ExpressionAttributeValues={
                ':empty_list': {'L': []},
                ':new_like': {'L': [{'M': like}]}
            }
        )
    else:
        like = 'already liked'
    
    
