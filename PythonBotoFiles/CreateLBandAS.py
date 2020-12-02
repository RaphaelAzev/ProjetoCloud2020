import boto3
import sys
from botocore.exceptions import ClientError
import time

ec2 = boto3.client('ec2', region_name='us-east-1')

secgrp = 'SecurityProjeto'


#Pega Id do security group que vai ser usado
try:
    response = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'group-name',
                'Values': [
                    secgrp,
                ],
            },
        ],
    )
    group_id = response['SecurityGroups'][0]['GroupId']
except ClientError as e:
    print(e)



Lista_subnets = []
secgrp_id = group_id



#Ver as subnets
try:
    print('Pegando subnets')
    response = ec2.describe_subnets()
    #print(response)
except ClientError as e:
    print(e)

for nets in response['Subnets']:
    print(nets['SubnetId'])
    Lista_subnets.append(nets['SubnetId'])



elb = boto3.client('elbv2', region_name='us-east-1')

#Cria Load Balancer usando as subnets descritas
try:
    print('Criando Load Balancer')
    response = elb.create_load_balancer(
        Name='LBprojeto',
        Subnets=Lista_subnets,
        SecurityGroups=[
            secgrp_id
        ],
        Tags=[
        {
            'Key': 'Projeto',
            'Value': 'ProjetoRapha'
        },
    ],
        Type='application',
    )
    LBalancerArn = response['LoadBalancers'][0]['LoadBalancerArn']
except ClientError as e:
    print(e)



waiter = elb.get_waiter('load_balancer_available') #Waiter para o load balancer criado

#Esperar Load Balancer ficar available
print('Esperando Load Balancer ficar Available')
waiter.wait(Names=['LBprojeto'])
print('LoadBalancer Available')



#Cria target group para esse Load Balancer
try:
    targetname = 'TargetProjeto'
    vpc = 'vpc-3e824f44'
    print('Criando Target Group ')
    response = elb.create_target_group(
        Name=targetname,
        Protocol='HTTP',
        Port=8080,
        VpcId=vpc,
        TargetType='instance',
        Tags=[
            {
                'Key': 'Projeto',
                'Value': 'ProjetoRapha'
            }
        ]
    )
    print('Target group ' + targetname + ' criado')
    targetgroupArn = response['TargetGroups'][0]['TargetGroupArn']
except ClientError as e:
    print(e)

time.sleep(5)




#Cria Listener para o Load Balancer
try:
    print('Criando Listener')
    response = elb.create_listener(
        LoadBalancerArn=LBalancerArn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': targetgroupArn,
            }
        ]
    )
    time.sleep(15)
    print('Listener Criado com sucesso')
except ClientError as e:
    print(e)





#Pega ID da AMI criada
AMIname = 'ORM Image'
try:
    print('Resgatando ID da imagem para ser usada no launch configuration')
    response = ec2.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [
                    AMIname
                ]
            }
        ]
    )
    image_id = response['Images'][0]['ImageId']
except ClientError as e:
    print(e)



ascl = boto3.client('autoscaling')

#Cria Lanuch Template para usar no autoscaling depois
LaunchConfigName = 'LaunchConfigProjeto'
try:
    print('Criando launch configuration')
    response = ascl.create_launch_configuration(
        LaunchConfigurationName=LaunchConfigName,
        ImageId=image_id,
        KeyName='Rapha_Cloud',
        SecurityGroups=[
            secgrp_id,
        ],
        InstanceType='t2.micro',
    )
    print('Launch Configuration ' + LaunchConfigName + ' criada')

except ClientError as e:
    print(e)

time.sleep(10)


#Montar string para o paramentro VPCZoneIndentifier
VPCzone = Lista_subnets[0]

for x in Lista_subnets[1:]:
    VPCzone += f', {x}'


#Cria autoscaling group usando a launch config
AScalename = 'AutoScalingProjeto'
try:
    print('Criando o autoscaling group ' + AScalename)
    response = ascl.create_auto_scaling_group(
        AutoScalingGroupName=AScalename,
        LaunchConfigurationName=LaunchConfigName,
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=2,
        TargetGroupARNs=[
            targetgroupArn,
        ],
        PlacementGroup='string',
        VPCZoneIdentifier=VPCzone,
        Tags=[
            {
                'Key': 'Projeto',
                'Value': 'ProjetoRapha'
            },
        ],
    )
    time.sleep(15)
    print('Autoscaling group criado')
except ClientError as e:
    print(e)
