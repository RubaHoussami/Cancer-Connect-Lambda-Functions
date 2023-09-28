import json 
import boto3
from boto3.dynamodb.conditions import Key
from functools import reduce

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

def remove(string):
    return reduce(lambda x, y: (x+y) if (y != " ") else x, string, "");
     
def lambda_handler (event, context):
    
    print(event)
    
    body = json.loads(event['body'])
    
    try:
        
        print("Make table.put_item call")
        
        response = table.query(KeyConditionExpression=Key('ID').eq(body['ID']))
        
        if 'Items' in response and len(response['Items']) > 0 :
            if remove(body['body'])!="":
                item = response['Items'][0]
                
                item['comments_dictionary'].append({
                    'user': body['user'],
                    'body': body['body']
                })
                
                # Update the item in DynamoDB
                table.update_item(
                    Key={'ID': body['ID'],
                        'timestamp' : body['timestamp']},
                    UpdateExpression='SET comments_dictionary = :val',
                    ExpressionAttributeValues={':val': item['comments_dictionary']}
                )
                
                item['comment_count']+=1
                
                # Update the item in DynamoDB
                table.update_item(
                    Key={'ID': body['ID'],
                        'timestamp' : body['timestamp']},
                    UpdateExpression='SET comment_count = :val',
                    ExpressionAttributeValues={':val': item['comment_count']}
                )
                
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Comment successfully added to dynamodb!"}) 
                }
                
            return {
                "statusCode" : 404,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Comment empty!"})
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
            "body" : json.dumps({"message" : "Internal server error!"})
        }