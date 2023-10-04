import json 
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal


dynamodb = boto3.resource('dynamodb')
table_name = 'Campaigns'
table = dynamodb.Table(table_name)


def lambda_handler (event, context): 
    
    body = json.loads(event['body'])
    body['amount']=Decimal(body['amount'])
    
    try:
        
        response = table.query(KeyConditionExpression=Key('ID').eq(body['ID']))
        
        if 'Items' in response and len(response['Items']) > 0:
            
            item = response['Items'][0]
            
            if body['amount']>0 and item['Current_amount'] + body['amount'] < item['Campaign_target']:
                
                item['Current_amount']+=body['amount']
                
                table.update_item(
                    Key={'ID': body['ID']},
                    UpdateExpression='SET Current_amount = :val',
                    ExpressionAttributeValues={':val': item['Current_amount']}
                )
                
                item['donations']+=1
                
                table.update_item(
                    Key={'ID': body['ID']},
                    UpdateExpression='SET donations = :val',
                    ExpressionAttributeValues={':val': item['donations']}
                )
        
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Donated!"}) 
                }
                
            elif body['amount']>0 and item['Current_amount'] + body['amount'] == item['Campaign_target']:
                
                item['Current_amount']=item['Campaign_target']
                
                table.update_item(
                    Key={'ID': body['ID']},
                    UpdateExpression='SET Current_amount = :val',
                    ExpressionAttributeValues={':val': item['Current_amount']}
                )
                
                item['donations']+=1
                
                table.update_item(
                    Key={'ID': body['ID']},
                    UpdateExpression='SET donations = :val',
                    ExpressionAttributeValues={':val': item['donations']}
                )
        
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Congradulations!"}) 
                }
                
            elif body['amount']>0 and item['Current_amount'] + body['amount'] > item['Campaign_target']:
                
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Thank you for the generous offer, but the donation amount exceeds the target amount!"}) 
                }
                
            return {
                "statusCode" : 404,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Amount cannot be negative!"})
            }
                
        return {
                "statusCode" : 404,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Campaign not found!"})
                }
    
    except Exception as e:
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }