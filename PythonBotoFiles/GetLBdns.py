import boto3
from botocore.exceptions import ClientError

elb = boto3.client('elbv2', region_name='us-east-1')

LBName = 'LBprojeto'

#Pega DNS do load balancer do projeto
try:
    response = elb.describe_load_balancers(Names=[LBName])
    with open('./LoadDNS.txt', 'w') as arq:
        arq.write(response['LoadBalancers'][0]['DNSName'])
except ClientError as e:
    print(e)

