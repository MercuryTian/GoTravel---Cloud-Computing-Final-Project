import json
import boto3

db_client = boto3.client('dynamodb')

def construct_item(event):
    
    item = {}

    if 'storyID' in event and event['storyID']:
        item['storyID'] = {'S': event['storyID']}
        
    if 'title' in event and event['title']:
        item['title'] = {'S': event['title']}

    if 'text' in event and event['text']:
        item['text'] = {'S': event['text']}

    if 'pic' in event and event['pic']:
        item['picture'] = {'S': event['pic']}

    if 'userID' in event and event['userID']:
        item['userID'] = {'S': event['userID']}
        
    if 'location' in event and event['location']:
        item['location'] = {'M': {'latitude': {'N': str(event['location']['latitude'])}, 'longitude': {'N': str(event['location']['longitude'])}}}
        
    if 'tags' in event and event['tags']:
        tag_list = []
        for tag in event['tags']:
            tag_list.append({'S': tag})
        item['tags'] = {'L': tag_list}

    if 'time' in event and event['time']:
        item['timestamp'] = {'S': event['time']}
    
    return item        

def lambda_handler(event, context):
    
    item = construct_item(event)
    
    db_client.put_item(
        TableName='gotravel-stories',
        Item=item
    )
    
    
