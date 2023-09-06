import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = 'Post'
table = dynamodb.Table(table_name)


def lambda_handler (event, context):
    
    # takes as input username, body, title
    print(event)
    
    body = json.loads(event['body'])
    try:
        
        new_post={
            'ID': uuid.uuid4().hex,
            'title' : body['title'],
            'body' : body['body'],
            'comments_dictionary' : [],
            'username' : "user"
        }
        
        print("Make table.put_item call")
        response=table.put_item(Item=new_post)
        
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
