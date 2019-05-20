from __future__ import print_function

import os
import json
import boto3
from botocore.vendored import requests

ES_HOST = 'https://search-chatbot-uixr6ui6jnxpkzvpxp6ad76bpa.us-east-1.es.amazonaws.com'
ES_INDEX = 'recommendations'
ES_TYPE = 'Recommendation'
REGION = 'us-east-1'

def lambda_handler(event, context):
    print("EVENT --- {}".format(event))
    headers = { "Content-Type": "application/json" }
    # query = event["queryStringParameters"]["tags"]
    query = event["tags"]
    
    url = ES_HOST + '/' + ES_INDEX + '/' + ES_TYPE + '/_search?q=' + str(query)
    es_response = requests.get(url, headers=headers).json()
    recommends = es_response["hits"]["hits"]

    print("ES_RESPONE RECOMMENDS --- {}".format(recommends))

    response = []
    for place in recommends:
        if place['_source']['label'] == 1:
            longtitude = place['_source']['longitude']
            latitude = place['_source']['latitude']
            response.append({"longitude": longtitude, "latitude": latitude})
    
    
    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         "Access-Control-Allow-Origin": "*"
    #     },
    #     'body': json.dumps(response)
    # }
    
    return response
