import boto3
import sys
from botocore.exceptions import ClientError
import time

ec2 = boto3.client('ec2', region_name='us-east-2')

#Pega IP da Instancia do PostGres
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
    DB_instance_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
except ClientError as e:
    print(e)

user_data = f'''#!/bin/bash
sudo apt update
cd /home/ubuntu
git clone https://github.com/RaphaelAzev/tasks.git
cd tasks
sed -i "s/'HOST': 'node1'/'HOST': '{DB_instance_ip}'/" /home/ubuntu/tasks/portfolio/settings.py 
./install.sh
sudo reboot'''

ec2 = boto3.client('ec2', region_name='us-east-1')

key_name = 'Rapha_Cloud'
secgrp = 'SecurityProjeto'
ubuntu18_AMI = 'ami-00ddb0e5626798373'
instance_name = 'ORM-Django'

#Cria instancia
try:
    print('Criando instancia')
    response = ec2.run_instances(
        ImageId=ubuntu18_AMI,
        InstanceType='t2.micro',
        KeyName=key_name,
        SecurityGroups=[secgrp],
        UserData=user_data,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    },
                    {
                        'Key': 'Projeto',
                        'Value': 'ProjetoRapha'
                    },
                ]
            }
        ],
        MaxCount=1,
        MinCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print('Instancia ' + instance_name + ' criada com sucesso')
except ClientError as e:
    print(e)

#Espera o status da instancia estar OK antes de criar a AMI
waiter = ec2.get_waiter('instance_status_ok')

print('Esperando instancia ficar OK')

waiter.wait(InstanceIds=[instance_id])

print('Instancia OK')

time.sleep(20)

#Cria AMI da instancia
waiter = ec2.get_waiter('image_available') #waiter da AMI para dar wait depois
AMIname = 'ORM Image'

try:
    print('Criando AMI da instancia...')
    response = ec2.create_image(
        Description='ORM AMI projeto',
        InstanceId=instance_id,
        Name=AMIname
    )
    image_id = response['ImageId']
except ClientError as e:
    print(e)

waiter.wait(ImageIds=[image_id])

print('AMI criada e disponivel')

#Termina instancia do ORM django usada para criar a AMI
try:
    print('Terminando instancia ' + instance_name)
    response = ec2.terminate_instances(
        InstanceIds=[
            instance_id,
        ]
    )   
except ClientError as e:
    print(e)

time.sleep(5)
