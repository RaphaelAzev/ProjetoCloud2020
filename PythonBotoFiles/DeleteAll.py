import boto3
import sys
from botocore.exceptions import ClientError
import time

#Script de limpar ambiente:
#Deletar Autoscaling
#Deletar Launch Configuration
#Deletar Load Balancer (listener eh deletado junto)
#Deletar Target group
#Deletar AMI
#Deletar Instancias (tag Projeto valor ProjetoRapha) (Lembrar DataBase em us-east-2 Djangos em us-east-1)
#Deletar SecurityGroup

ascl = boto3.client('autoscaling', region_name='us-east-1') #Client para AutoScaling

elb = boto3.client('elbv2', region_name='us-east-1') #Client para Load Balancing

ec2NV = boto3.client('ec2', region_name='us-east-1') #Client para EC2 (North Virginia)

ec2OH = boto3.client('ec2', region_name='us-east-2') #Client para EC2 (Ohio)

#Deleta Auto Scaling Group
AScalename = 'AutoScalingProjeto'
try:
    print('Deletando Auto Scaling Group')
    response = ascl.delete_auto_scaling_group(
        AutoScalingGroupName=AScalename,
        ForceDelete=True
    )
    time.sleep(25)
except ClientError as e:
    print(e)
    print('Nao ha autoscaling group para deletar')

#Deleta Instancia de Ohio
Lista_instanciasOH = []
waiterOhio = ec2OH.get_waiter('instance_terminated') #Waiter para esperar a instancia ser terminada

try:
    print('Deletando instancias de Ohio')
    response = ec2OH.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
            {
                'Name': 'tag:Projeto',
                'Values': [
                    'ProjetoRapha',
                ]
            }
        ]
    )
    #print(response)
    try:
        for x in response['Reservations'][0]['Instances']:
            Lista_instanciasOH.append(x['InstanceId'])
        response = ec2OH.terminate_instances(InstanceIds=Lista_instanciasOH)
        waiterOhio.wait(InstanceIds=Lista_instanciasOH)
        print('Instancias deletadas')
    except:
        print('Nao ha instancias a deletar')

except ClientError as e:
    print(e)

#Deleta Instancias de NV se existirem
Lista_instanciasNV = []
waiterNV = ec2NV.get_waiter('instance_terminated') #Waiter para esperar a instancia ser terminada

try:
    print('Deletando instancias de NV')
    response = ec2NV.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
            {
                'Name': 'tag:Projeto',
                'Values': [
                    'ProjetoRapha',
                ]
            }
        ]
    )
    #print(response)
    try:
        for x in response['Reservations'][0]['Instances']:
            Lista_instanciasNV.append(x['InstanceId'])
        response = ec2NV.terminate_instances(InstanceIds=Lista_instanciasOH)
        waiterNV.wait(InstanceIds=Lista_instanciasOH)
        print('Instancias deletadas')
    except:
        print('Nao ha instancias a deletar')

except ClientError as e:
    print(e)


#Deleta Launch Configuration
LaunchConfigName = 'LaunchConfigProjeto'
try:
    print('Deletando Launch Configuration')
    response = ascl.delete_launch_configuration(
        LaunchConfigurationName=LaunchConfigName
    )
    time.sleep(15)
except ClientError as e:
    print(e)
    print('Nao ha Launch Config para deletar')



#Deleta Load Balancer
waiter = elb.get_waiter('load_balancers_deleted') #Waiter para esperar o Load Balancer ser deletado
LBname = 'LBprojeto'
LBArn = ''

#Pega ARN do LB para deleta-lo
try:
    response = elb.describe_load_balancers(Names=[LBname])
    LBArn = response['LoadBalancers'][0]['LoadBalancerArn']
except ClientError as e:
    print(e)
    

#Deleta
try:
    print('Deletando Load Balancer')
    response = elb.delete_load_balancer(LoadBalancerArn=LBArn)
    waiter.wait(Names=[LBname])
except ClientError as e:
    print(e)
    print('Nao ha Load Balancers para deletar')

time.sleep(10)
#Deleta Target Group

#Pega ARN do target group para deleta-lo
targetname = 'TargetProjeto'
TargetARN = ''
try:
    response = elb.describe_target_groups(Names=['TargetProjeto'])
    TargetARN = response['TargetGroups'][0]['TargetGroupArn']
except ClientError as e:
    print(e)

#Deleta
try:
    print('Deletando Target Group')
    response = elb.delete_target_group(
        TargetGroupArn=TargetARN
    )
    time.sleep(5)
except ClientError as e:
    print(e)
    print('Nao ha target group para deletar')


#Deleta AMI

#Pega ID da AMI
AMIname = 'ORM Image'
image_id = ''

try:
    response = ec2NV.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [
                    AMIname
                ]
            }
        ]
    )
    try:
        image_id = response['Images'][0]['ImageId']
    except:
        pass
except ClientError as e:
    print(e)

#Deleta AMI usando o ID
try:
    print('Deletando AMI')
    response = ec2NV.deregister_image(
        ImageId=image_id
    )
    print('AMI deregistrada')
except ClientError as e:
    print(e)
    print('Nao ha AMI para deletar')


#Deleta as instancias referentes ao projeto
#Lista_instanciasNV = []

#North Virginia primeiro (nao precisa pois deletar o Auto scaling group deleta as instancias)
#try:
#    print('Deletando instancias de North Virginia')
#    response = ec2NV.describe_instances(
#        Filters=[
#            {
#                'Name': 'instance-state-name',
#                'Values': [
#                    'running',
#                ]
#            },
#            {
#                'Name': 'tag:Projeto',
#                'Values': [
#                    'ProjetoRapha',
#                ]
#            }
#        ]
#    )
#    try:
#        for x in response['Reservations'][0]['Instances']:
#            Lista_instanciasNV.append(x['InstanceId'])
#        response = ec2NV.terminate_instances(InstanceIds=Lista_instanciasNV)
#    except:
#        pass
#
#    time.sleep(10)
#    print('Instancias deletadas')
#except ClientError as e:
#    print(e)


#Deleta Security Group
secgrp = "SecurityProjeto"

#North Virginia primeiro
try:
    print('Deletando Security Group de North Virginia')
    response = ec2NV.delete_security_group(GroupName = secgrp)
    time.sleep(5)
     
except ClientError as e:
        print(e)

#Por final Ohio
try:
    print('Deletando Security Group de Ohio')
    response = ec2OH.delete_security_group(GroupName = secgrp)
     
    time.sleep(5)
except ClientError as e:
        print(e)


time.sleep(30)