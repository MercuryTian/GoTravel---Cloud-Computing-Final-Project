import json
import boto3
from story_parse import parse

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    id = event['storyId']
    
    try:
        story = dynamodb_client.get_item(
            TableName='gotravel-stories',
            Key={
                'storyID': {
                    'S': id
                }
            },
        )['Item']
    except:
        story = {}
    
    story_parsed = parse(story)
    
    
    return story_parsed