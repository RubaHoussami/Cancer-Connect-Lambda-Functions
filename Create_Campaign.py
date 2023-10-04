import json 
import boto3
import random
from decimal import Decimal
from functools import reduce 


def remove(string):
    return reduce(lambda x, y: (x+y) if (y != " ") else x, string, "");
    

dynamodb = boto3.resource('dynamodb')
table_name = 'Campaigns'
table = dynamodb.Table(table_name)


def lambda_handler (event, context):
    
    body = json.loads(event['body']) 
    
    try:
         
        if remove(body['title'])!="" and remove(body['description'])!="" and remove(body['name'])!="":
                        
            new_post={
                'ID': "".join([str(random.randint(0, 9)) for _ in range(6)]),
                'Campaign_title' : body['title'],
                'Campaign_description' : body['description'],
                'name' : body['name'],
                'Campaign_target' : Decimal(body['target']),
                'donations' : 0,
                'Current_amount' : Decimal(0)
            }
            
            response=table.put_item(Item=new_post)
            
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            
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
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }