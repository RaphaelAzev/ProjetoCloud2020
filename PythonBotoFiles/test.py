import boto3
import sys
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='us-east-2')


#Checa se existe
try:
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'PostgresDB',
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            }
        ]
    )
    instance_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(instance_ip)
except: 
    print("hi")