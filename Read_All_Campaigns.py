import json
import boto3 


dynamodb = boto3.resource('dynamodb')
table_name = 'Campaigns'
table = dynamodb.Table(table_name)


def lambda_handler (event, context):  
    
    try:
        response = table.scan()
        
        for item in response['Items']:
            item['donations']=str(item['donations'])
            item['Campaign_target']=str(item['Campaign_target'])
            item['Current_amount']=str(item['Current_amount'])
        
        return {
            "statusCode" : 200, # OK - success
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps(response['Items']) 
        }
            
    except Exception as e:
        return {
            "statusCode" : 500, # internal server error - failure
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"}) 
        }