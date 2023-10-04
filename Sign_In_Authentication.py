import json
import boto3
import hashlib
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table_name = 'Authentication'
table = dynamodb.Table(table_name)


def hash(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    return hash_object.hexdigest()

def lambda_handler(event, context):
    
    body=json.loads(event['body'])
    
    try:
        
        response = table.query(KeyConditionExpression=Key('username').eq(body['username']))
        
        if 'Items' in response and len(response['Items']) > 0:
            if hash(body['password']) == response['Items'][0]['password']:
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Welcome to Cancer Connect!"}) 
                }
            return {
                "statusCode" : 404,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Incorrect username or password."})
            }
        return {
            "statusCode" : 404,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Incorrect username or password."})
        }
    
    except Exception as e:
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }