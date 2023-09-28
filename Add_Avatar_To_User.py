import json
import boto3
from boto3.dynamodb.conditions import Key
 
dynamodb = boto3.resource('dynamodb')
table_name = 'Authentication' 
table = dynamodb.Table(table_name)

def lambda_handler (event, context):
    
    print(event)
    
    body = json.loads(event['body'])
    
    try:
        
        response = table.query(KeyConditionExpression=Key('username').eq(body['userr']))
        
        if 'Items' in response and len(response['Items']) > 0:
            item = response['Items'][0]
            
            item['avatar']=body['avatar']
            
            # Update the item in DynamoDB
            table.update_item(
                Key={'username' : body['userr']},
                UpdateExpression='SET avatar = :val',
                ExpressionAttributeValues={':val': item['avatar']}
            )
            
            return {
                "statusCode" : 200,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Avatar successfully added to dynamodb!"}) 
            }
                
        return {
                "statusCode" : 404,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "User not found!"})
                }
      
    # catch any other errors due to accessing data
    
    except Exception as e:
        print(e)
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }