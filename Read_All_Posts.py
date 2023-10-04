import json
import boto3 
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

table_name1 = 'Authentication'
table1 = dynamodb.Table(table_name1)


def lambda_handler (event, context):  
    
    try:
        
        response1 = table1.query(KeyConditionExpression=Key('username').eq(event['rawPath'][1:]))
         
        response = table.scan()
        
        for i in range(1, len(response['Items'])): 
            key = response['Items'][i]
            j = i-1
            while j >= 0 and int(key['timestamp']) >= int(response['Items'][j]['timestamp']):  
                response['Items'][j+1] = response['Items'][j]
                j -= 1
            response['Items'][j+1] = key
        
        likes=[]
        
        for item in response['Items']:
            item['comment_count']=str(item['comment_count'])
            item['avatar']=str(item['avatar'])
            likes.append(str(item['likes']))
            item['likes']=str(item['likes'])
        
        response['liked_posts']=response1['Items'][0]['liked_posts']
        response['badges']=response1['Items'][0]['badges']
        response['likes']=likes
    
        return {
            "statusCode" : 200,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps(response) 
        }
            
    except Exception as e:
        return {
            "statusCode" : 500, # internal server error - failure
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"}) 
        }