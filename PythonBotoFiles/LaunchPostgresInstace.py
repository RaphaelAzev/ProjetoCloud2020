import boto3
import sys
from botocore.exceptions import ClientError

user_data = '''#!/bin/bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud'; "
sudo -u postgres createdb -O cloud tasks
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'\t/" /etc/postgresql/10/main/postgresql.conf
echo "host    all             all             0.0.0.0/0               trust" >> /etc/postgresql/10/main/pg_hba.conf
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql'''

ec2 = boto3.client('ec2', region_name='us-east-2')

key_name = 'Rapha_Cloud'
secgrp = 'SecurityProjeto'
ubuntu18_AMI = 'ami-0dd9f0e7df0f0a138'
instance_name = 'PostgresDB'

#Cria instancia
try:
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