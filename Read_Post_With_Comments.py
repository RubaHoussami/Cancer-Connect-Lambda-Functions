import json
import boto3
from boto3.dynamodb.conditions import Key
 
dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

table_name1 = 'Authentication'
table1 = dynamodb.Table(table_name1)

def lambda_handler (event, context):
    
    print(event)
    
    post_id = event['rawPath'][1:]
    
    try:  
        
        print("Make table.put_item call")
        
        response = table.query(KeyConditionExpression=Key('ID').eq(post_id))
        print(response)
        
        if 'Items' in response and len(response['Items']) > 0: 
            
            response['Items'][0]['likes']=str(response['Items'][0]['likes'])
            response['Items'][0]['comment_count']=str(response['Items'][0]['comment_count'])
            response['Items'][0]['avatar']=str(response['Items'][0]['avatar'])
            
            response1 = table1.query(KeyConditionExpression=Key('username').eq(response['Items'][0]['username']))
            print(response1)
            
            print(response)
            if post_id in response1['Items'][0]['liked_posts']:
                response['Items'][0]['liked_or_no']="1"
            else:
                response['Items'][0]['liked_or_no']="0"
            print(response)
            return {
                "statusCode" : 200,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps(response) 
            }
                
        return {
            "statusCode" : 404,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Post not found!"})
        }
      
    # catch any other errors due to accessing data
    
    except Exception as e:
        print(e)
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : str(event)})
        }