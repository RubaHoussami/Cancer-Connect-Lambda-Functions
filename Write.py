import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

def lambda_handler (event, context):
    
    print(event)
    
    try:
        
        response=table.put_item(Item=event)
        print(response)
        
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
        
        print(e)
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }
