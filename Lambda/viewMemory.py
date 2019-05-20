import json
import boto3
from datetime import datetime, timedelta
from story_parse import parse

dynamodb_client = boto3.client('dynamodb')

def get_stories(userID, time, range):
    result = []
    time_now = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    earliest = time_now - timedelta(days=range)
    items = dynamodb_client.scan(TableName='gotravel-stories')['Items']
    for item in items:
        if item['userID']['S'] == userID:
            my_story = True
        else:
            my_story = False
        if datetime.strptime(item['timestamp']['S'], '%Y-%m-%d %H:%M:%S') >= earliest:
            in_range = True
        else:
            in_range = False
        if my_story and in_range:
            result.append(item)
    return result

def lambda_handler(event, context):
    userID = event['userId']
    time = event['time']
    range = event['range'] # in days
    
    stories = get_stories(userID, time, int(range))
    
    stories_parsed = [parse(x) for x in stories]

    '''
    return {
        'statusCode': 200,
        'body': stories_parsed
    }
    '''
    return stories_parsed
