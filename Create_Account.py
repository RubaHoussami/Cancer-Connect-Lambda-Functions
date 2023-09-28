import json
import boto3
import hashlib

def hash(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    return hash_object.hexdigest()

dynamodb = boto3.resource('dynamodb')
table_name = 'Authentication'
table = dynamodb.Table(table_name)


#when creating the account, use to make sure the username is not found in database already and that password is valid

def lambda_handler (event, context):
    print(event)
    body=json.loads(event['body'])
    print(body)
    
    try:
        #checking for username requirements
        
        if body['username']=="":

            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Please enter a username!"}) 
            }
            
        response = table.scan()
        print(response)
        
        usernames=[]
        for item in response['Items']:
            usernames.append(item['username'])
            
        if body['username'] in usernames:

            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Username has already been taken!"}) 
            }
            
        if len(body['password'])<7:
            
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Password needs to be at least 7 characters!"}) 
            }
        
        # checking for password requirements
        if body['password']!=body['confirm_password']:
            
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Passwords do not match!"}) 
            }
        
        countlower=0
        countupper=0
        countnumber=0
        countspecial=0
        
        for i in body['password']:
            if ord(i) in [k for k in range(65, 91)] + [k for k in range(97, 123)]:
                if(i.islower()):
                    countlower+=1
                if (i.isupper()):
                    countupper+=1
            elif i in ["0","1","2","3","4","5","6","7","8","9"]:
                countnumber+=1
            else:
                countspecial+=1
                
        if countlower==0:
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Password must contain at least one lowercase character!"}) 
            }
        
        if countupper==0:
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Password must contain at least one uppercase character!"}) 
            }
        
        if countnumber==0:
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Password must contain at least one number!"}) 
            }
        
        if countspecial==0:
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Password must contain at least one special character!"}) 
            }
            
            
        if '@' not in body['email'] or '.' not in body['email']:
            return {
                "statusCode" : 400,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Please enter a valid email address!"}) 
            }

        new_post={ 
            'Day':body['Day'],
            'Month':body['Month'],
            'Year':body['Year'],
            'email' : body['email'],
            'First_name' : body['First_name'],
            'Last_name' : body['Last_name'],
            'password' : hash(body['password']),
            'Phone_Number' : body['Phone_Number'],
            'username' : body['username'],
            'liked_posts' : [],
            'avatar' : 0
        }
        
        if body['Badge']=="1":
            new_post["badges"] = ['1']
        elif body['Badge']=="2":
            new_post["badges"] = ['2']
        elif body['Badge']=="3":
            new_post["badges"] = ['3']
        else:
            new_post["badges"] = ['4']
        
        response2=table.put_item(Item=new_post)
        print(response2)
        
        if response2['ResponseMetadata']['HTTPStatusCode'] == 200: # checking for success
            return {
                "statusCode" : 200,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Account created!"}) 
            }
            
        else:
            return {
                "statusCode" : 500,
                "headers" : {"Content-Type":"application/json"},
                "body" : json.dumps({"message" : "Failed to create account!"})
                }
            
    except Exception as e:
        print(e)
        return {
            "statusCode" : 500, # internal server error - failure
            "headers" : {"Content-Type":"application/json"},
            "body" : json.dumps({"message" : "Internal server error!"}) 
        }
        
      