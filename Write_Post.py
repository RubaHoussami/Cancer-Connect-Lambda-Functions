import json 
import boto3
import uuid
from datetime import datetime 
from boto3.dynamodb.conditions import Key
from functools import reduce 
 
def remove(string):
    return reduce(lambda x, y: (x+y) if (y != " ") else x, string, "");
     

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

table_name1 = 'Authentication' 
table1 = dynamodb.Table(table_name1)


def lambda_handler (event, context):
    
    body = json.loads(event['body'])
    
    try:
        current_time = str(datetime.now().isoformat())
        current=current_time[0:4]+current_time[5:7]+current_time[8:10]+current_time[11:13]+current_time[14:16]+current_time[17:19]
        
        response1=table1.query(KeyConditionExpression=Key('username').eq(body['username']))
        
        if remove(body['title'])!="" and remove(body['body'])!="":
            
            posts=table.scan()
            
            badge5=False
            counter=0 
            for post in posts['Items']:
                if post['username']==body['username']:
                    counter+=1 
            
            if counter+1==10 and '5' not in response1['Items'][0]['badges']:
                badge5=True 
                
                response1['Items'][0]['badges'].append('5')
                
                table1.update_item(
                    Key={'username': response1['Items'][0]['username']},
                    UpdateExpression='SET badges = :val',
                    ExpressionAttributeValues={':val': response1['Items'][0]['badges']}
                )
                        
            new_post={
                'ID': uuid.uuid4().hex,
                'title' : body['title'],
                'body' : body['body'],
                'comments_dictionary' : [],
                'username' : body['username'],
                'timestamp': current,
                'likes' : 0,
                'comment_count' : 0,
                'liked_users' : [],
                'avatar' : response1['Items'][0]['avatar'],
                'badges' : response1['Items'][0]['badges'][0]
            }
            
            response=table.put_item(Item=new_post)
            
            if response['ResponseMetadata']['HTTPStatusCode'] == 200 and badge5:
            
                return {
                    "statusCode" : 201,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Item successfully added to dynamodb and badge 5 earned!"}) 
                }
                
            elif response['ResponseMetadata']['HTTPStatusCode'] == 200:
            
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Item successfully added to dynamodb!"}) 
                }
                
            return {
                "statusCode" : 500,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Failed to add item to dynamodb!"})
            }
        return {
            "statusCode" : 404,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Empty message!"})
        }
    
    except Exception as e:
        print(e)
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }
