import json
import boto3
import hashlib
from boto3.dynamodb.conditions import Key


def hash(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    return hash_object.hexdigest()


dynamodb = boto3.resource('dynamodb')
table_name = 'Authentication'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    
    body = json.loads(event['body'])
    
    try:
        
        response = table.query(KeyConditionExpression=Key('username').eq(body['username']))
        
        if 'Items' in response and len(response['Items']) > 0:
            if body['password']==body['confirm_password']:
                
                item = response['Items'][0]
                
                item['password']=hash(body['password'])
                
                table.update_item(
                    Key={'username': body['username']},
                    UpdateExpression='SET comment_count = :val',
                    ExpressionAttributeValues={':val': item['password']}
                )
                
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Password successfully updated!"}) 
                }
                
            else:
                return {
                    "statusCode" : 400,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Passwords do not match!"})
                }
            
            return {
                "statusCode" : 500,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "User not found!"})
            }
        
    except Exception as e:
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }