import json
import boto3

db_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    item = {}
    item['userID'] = {'S': event['request']['userAttributes']['sub']}
    item['email'] = {'S': event['request']['userAttributes']['email']}
    item['username'] = {'S': event['request']['userAttributes']['preferred_username']}
    item['bio'] = {'S': event['request']['userAttributes']['custom:bio']}
    
    db_client.put_item(
        TableName='gotravel-users',
        Item=item
    )
    
    return event
    
    
