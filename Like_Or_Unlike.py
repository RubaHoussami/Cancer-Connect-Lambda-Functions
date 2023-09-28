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
    
    body = json.loads(event['body']) 
     
    try:
        
        response = table.query(KeyConditionExpression=Key('ID').eq(body['postId']))
        
        print(response)
         
        if 'Items' in response and len(response['Items']) > 0: 
            item = response['Items'][0]
            
            response1 = table1.query(KeyConditionExpression=Key('username').eq(body['username']))
            print(response1)
            if body['username'] not in item['liked_users']:
                
                print(response1['Items'][0]['liked_posts'])
                
                response1['Items'][0]['liked_posts'].append(body['postId'])
                
                table1.update_item(
                    Key={'username': body['username']},
                    UpdateExpression='SET liked_posts = :val',
                    ExpressionAttributeValues={':val': response1['Items'][0]['liked_posts']}
                )
                print(response1['Items'][0]['liked_posts'])
                
                print(item['likes'])
                item['likes']+=1
                
                print(item['likes'])
                
                # Update the item in DynamoDB
                table.update_item(
                    Key={'ID': body['postId'],
                        'timestamp' : body['timestamp']},
                    UpdateExpression='SET likes = :val',
                    ExpressionAttributeValues={':val': item['likes']}
                )
                
                print(item['likes'])
                print(item['liked_users'])
                item['liked_users'].append(body['username'])
                
                print(item['liked_users'])
                
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
            
            print(response1['Items'][0]['liked_posts'])
            response1['Items'][0]['liked_posts'].remove(body['postId'])
            print(response1['Items'][0]['liked_posts'])
            
            table1.update_item(
                Key={'username': body['username']},
                UpdateExpression='SET liked_posts = :val',
                ExpressionAttributeValues={':val': response1['Items'][0]['liked_posts']}
            )
            print(item['likes'])
            item['likes']-=1
            print(item['likes'])
            
            # Update the item in DynamoDB
            table.update_item(
                Key={'ID': body['postId'],
                    'timestamp' : body['timestamp']},
                UpdateExpression='SET likes = :val',
                ExpressionAttributeValues={':val': item['likes']}
            )
            
            print(item['liked_users'])
            item['liked_users'].remove(body['username'])
                
            table.update_item(
                Key={'ID': body['postId'],
                    'timestamp' : body['timestamp']},
                UpdateExpression='SET liked_users = :val',
                ExpressionAttributeValues={':val': item['liked_users']}
            )
            print(item['liked_users'])
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
      
    # catch any other errors due to accessing data
    
    except Exception as e: 
        print(e)
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : str(e)})
        }