import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

def lambda_handler (event, context):
    try:
        
        # checking if item exists in database
     
        response = table.scan()
        print(response)
        return {
                "statusCode" : 200, # OK - success
                "headers" : {"Content-Type":"application/json"}, # set the HTTP header of the response - JSON data
                "body" : json.dumps(response) # turn Python dictionary ito JSON string to be sent as response body
            }
            
    except Exception as e:
        print(e)
        return {
            "statusCode" : 500, # internal server error - failure
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"}) 
        }
