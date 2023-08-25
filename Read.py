import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

def lambda_handler (event, context):
    try:
        input_data=json.loads(event['body']) # dictionary containing item to be written
        
        response=table.set_item(input_data)
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200: # checking for success
        
            return {
                "statusCode" : 200,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Item successfully added to dynamodb!"}) 
            }
            
        else:
     
            return {
                "statusCode" : 500,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Failed to add item to dynamodb!"})
                }
      
    # catch any other errors due to accessing data
    
    except Exception as e:
     
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }
