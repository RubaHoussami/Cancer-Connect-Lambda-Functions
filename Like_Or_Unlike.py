import json
import boto3 
from boto3.dynamodb.conditions import Key

 
dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

table_name1 = 'Authentication' 
table1 = dynamodb.Table(table_name1)


def lambda_handler (event, context):
    
    body = json.loads(event['body']) 
     
    try:
        
        response = table.query(KeyConditionExpression=Key('ID').eq(body['postId']))
         
        if 'Items' in response and len(response['Items']) > 0: 
            item = response['Items'][0]
            
            response1 = table1.query(KeyConditionExpression=Key('username').eq(body['username']))
            
            if body['username'] not in item['liked_users']:
                
                response1['Items'][0]['liked_posts'].append(body['postId'])
                
                table1.update_item(
                    Key={'username': body['username']},
                    UpdateExpression='SET liked_posts = :val',
                    ExpressionAttributeValues={':val': response1['Items'][0]['liked_posts']}
                )
                
                item['likes']+=1
                
                table.update_item(
                    Key={'ID': body['postId'],
                        'timestamp' : body['timestamp']},
                    UpdateExpression='SET likes = :val',
                    ExpressionAttributeValues={':val': item['likes']}
                )
                
                item['liked_users'].append(body['username'])
                
                table.update_item(
                    Key={'ID': body['postId'],
                        'timestamp' : body['timestamp']},
                    UpdateExpression='SET liked_users = :val',
                    ExpressionAttributeValues={':val': item['liked_users']}
                )
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Post liked!"}) 
                }

            response1['Items'][0]['liked_posts'].remove(body['postId'])
            
            table1.update_item(
                Key={'username': body['username']},
                UpdateExpression='SET liked_posts = :val',
                ExpressionAttributeValues={':val': response1['Items'][0]['liked_posts']}
            )
            
            item['likes']-=1
            
            table.update_item(
                Key={'ID': body['postId'],
                    'timestamp' : body['timestamp']},
                UpdateExpression='SET likes = :val',
                ExpressionAttributeValues={':val': item['likes']}
            )
            
            item['liked_users'].remove(body['username'])
                
            table.update_item(
                Key={'ID': body['postId'],
                    'timestamp' : body['timestamp']},
                UpdateExpression='SET liked_users = :val',
                ExpressionAttributeValues={':val': item['liked_users']}
            )
            
            return {
                "statusCode" : 200,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Post unliked!"}) 
            }
                
        return {
            "statusCode" : 404,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Post not found!"})
        }
    
    except Exception as e:
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : str(e)})
        }