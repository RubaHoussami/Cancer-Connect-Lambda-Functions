import json
import boto3


dynamodb = boto3.resource('dynamodb')
table_name = 'Authentication'
table = dynamodb.Table(table_name)


def send_email(subject, body, recipient):
    response = ses.send_email(
        Source='cancercnnct@gmail.com',
        Destination={
            'ToAddresses': [recipient]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )
        
        
def lambda_handler(event, context):
    body=event['body']
    try:
        reponse=table.scan()
        for item in response['Items']:
            if body['username']==item['username'] and body['email']==item['email']:
                subject = "This is an automated email to update your password"
                body = "Hello, you are receiving this email to reset your Cancer Connect password. If you did not request this password change, you can ignore this email."
                recipient = body['email']
                send_email(subject, body, recipient)
                return {
                    "statusCode" : 200,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Email successfully sent!"})
                }
                
            elif body['username']==item['username'] and body['email']!=item['email']:
                return {
                    "statusCode" : 400,
                    "headers" : {"Content-Type":"application/json"},
                    "body" : json.dumps({"message" : "Wrong email address!"})
                }
                
        return {
            "statusCode" : 400,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Username not found!"})
        }
        
    except Exception as e:
        return {
            "statusCode" : 500,
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"})
        }