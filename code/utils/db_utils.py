import boto3
import os

KEY = os.getenv('DYNAMO_ACCESS_KEY_ID')
SECRET = os.getenv('DYNAMO_SECRET_ACCESS_KEY')

client = boto3.client(
    'dynamodb',
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
    region_name='eu-west-1'
)

def delete_user(chat_id):

    client.delete_item(
        TableName='fiemme_servizi_users',
        Key={
            'chat_id': {
                'N': str(chat_id)
            }
        }
    )    


def modify_user(chat_id, comune):

    client.update_item(
        TableName='fiemme_servizi_users',
        Key={
            'chat_id': {
                'N': str(chat_id)
            }
        },
        UpdateExpression='SET comune = :newComune',
        ExpressionAttributeValues={
            ':newComune': {
                'N': str(comune)
            }
        }
    )    

def add_user(chat_id, comune):
    
        #add user to table fiemme_servizi_users
        client.put_item(
            TableName='fiemme_servizi_users',
            Item={
                'chat_id': {
                    'N': str(chat_id)
                },
                'comune': {
                    'N': str(comune)
                }
            }
        )


def read_all_users():

    #read table fiemme_servizi_users
    users = client.scan(
        TableName='fiemme_servizi_users',
        Select='ALL_ATTRIBUTES'
    )

    return users



# main
if __name__ == '__main__':
    print('Testing')

    print(read_all_users())
