import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)

def lambda_handler (event, context):
    try:
       item_id = event['queryStringParameters']['ID']  # the partition key is the ID - no sort key (maybe we can add one?)
     
        # checking if item exists in database
     
        response = table.get_item{'ID':obj_id}
     
        if 'Item' in response:
            item = response['Item']
        
            # dictionary containing requested data
        
            extracted_item = {
                'ID' : item['ID'],
                'title' : item.get('title',''),
                'body' : item.get('body','')
            }
        
            return {
                "statusCode" : 200, # OK - success
                "headers" : {"Content-Type":"application/json"}, # set the HTTP header of the response - JSON data
                "body" : json.dumps(extracted_item) # turn Python dictionary ito JSON string to be sent as response body
            }
      
        else: # item not found
     
            return {
                "statusCode" : 404, # not found error - failure
                "headers" : {"Content-Type":"application/json"}, # set the HTTP header of the response - JSON data
                "body" : json.dumps({"message" : "Item not found!"}) # display message ig
                }
      
    # catch any other errors due to accessing data
    
    except Exception as e:
     
        return {
            "statusCode" : 500, # internal server error - failure
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"}) 
        }