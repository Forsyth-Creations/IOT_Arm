import boto3
from boto3.resources.factory import ServiceResource
from botocore.exceptions import ClientError
from colorama import Fore, Back, Style

# https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html

class dbHelper:
    def __init__(self):
        self.dynamodb : ServiceResource = boto3.resource('dynamodb', 
                    endpoint_url='http://localhost:8080', 
                    region_name='us-east-1', 
                    aws_access_key_id = "local",
                    aws_secret_access_key = "local")
        self.create_table("Users")
        self.create_table("Devices")

    def create_table_no_attr(self, name : str):
        try:
            self.dynamodb.create_table(
                TableName=name,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        except Exception as e:
            print(e)

    def create_table(self, name : str):
        try:
            self.dynamodb.create_table(
                TableName=name,
                KeySchema=[
                    {
                        'AttributeName': 'uid',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'uid',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        except Exception as e:
            print(e.response['Error']['Message'] + " : " + name)
    
    def get_table(self, name : str):
        return self.dynamodb.Table(name)
    
    def add_entry(self, table, item):
        table.put_item(Item=item)

    def get_entry(self, table, entry : dict):
        key = entry.keys()[0]
        value = entry[key]
        table.query(KeyConditionExpression=Key(key).eq(entry[value]))