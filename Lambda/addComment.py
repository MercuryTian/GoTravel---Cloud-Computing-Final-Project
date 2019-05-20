import json
import boto3

db_client = boto3.client('dynamodb')

def construct_comment(text, time, userID):
    comment = {}
    comment['text'] = {'S': text}
    comment['time'] = {'S': time}
    comment['userID'] = {'S': userID}
    return comment

def lambda_handler(event, context):
    text = event['text']
    time = event['time']
    userID = event['userID']
    storyID = event['storyID']
    
    comment = construct_comment(text, time, userID)
    db_client.update_item(
        TableName='gotravel-stories',
        Key={
            'storyID': {
                'S': storyID
            }
        },
        UpdateExpression='SET comments = list_append(if_not_exists(comments, :empty_list), :new_comment)',
        ExpressionAttributeValues={
            ':empty_list': {'L': []},
            ':new_comment': {'L': [{'M': comment}]}
        }
    )
    
    
