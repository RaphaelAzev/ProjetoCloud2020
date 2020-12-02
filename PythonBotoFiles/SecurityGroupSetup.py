import boto3
from botocore.exceptions import ClientError
import time

ec2 = boto3.client('ec2', region_name='us-east-1')

print("Configurando security group para a regiao us-east-1 (NorthVirginia)")

#Create Security Group
secgrp = "SecurityProjeto"

try:
    response = ec2.create_security_group(
        Description='Security Group Projeto NorthVirginia',
        GroupName=secgrp,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Projeto',
                        'Value': 'ProjetoRapha'
                    },
                ]
            },
        ],
    )
    new_group_id = response['GroupId']
    print('Security Group ' + secgrp + ' criado')
except ClientError as e:
    print("Erro ao criar o security group")
    print(e)

try:
    print("Adicionando regras")
    data = ec2.authorize_security_group_ingress(
        GroupId=new_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 8080,
             'ToPort': 8080,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 5432,
             'ToPort': 5432,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    print("Regras corretamente adicionadas ao grupo")
except ClientError as e:
    print(e)


ec2 = boto3.client('ec2', region_name='us-east-2')

print("Configurando security group para a regiao us-east-2 (Ohio)")

#Create Security Group
secgrp = "SecurityProjeto"

try:
    response = ec2.create_security_group(
        Description='Security Group Projeto Ohio',
        GroupName=secgrp,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Projeto',
                        'Value': 'ProjetoRapha'
                    },
                ]
            },
        ],
    )
    new_group_id = response['GroupId']
    print('Security Group ' + secgrp + ' criado')
except ClientError as e:
    print("Erro ao criar o security group")
    print(e)

try:
    print("Adicionando regras")
    data = ec2.authorize_security_group_ingress(
        GroupId=new_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 8080,
             'ToPort': 8080,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 5432,
             'ToPort': 5432,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}        
        ]
    )
    print("Regras corretamente adicionadas ao grupo")
except ClientError as e:
    print(e)

time.sleep(20)