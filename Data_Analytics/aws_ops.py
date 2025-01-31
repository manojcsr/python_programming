from dotenv import load_dotenv
load_dotenv()
import os
import boto3

def get_aws_session():
    aws_access_key_id=os.environ['AWS_ACCESS_KEY']
    aws_secret_access_key=os.environ['AWS_SECRET_KEY']
    region_name=os.environ['AWS_REGION']

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    return session

def create_instances(
    image_id='ami-03a6b9092d0d03aab', # Amazon Linux 2 AMI
    min_count=1, max_count=1, 
    instance_type='t2.micro', key_name='ec2-key-pair'
):    
    # Launch EC2 instance
    instances = ec2_client.create_instances(
        ImageId=image_id, 
        MinCount=min_count,
        MaxCount=max_count, # Both MinCount and MaxCount are mandatory
        InstanceType=instance_type,
        KeyName=key_name
    )

    return instances


#################### MAIN ####################
session = get_aws_session()

print(session)

# Create EC2 resource
ec2_client = session.resource('ec2')

# spin a server for k8s master
create_instances(instance_type='t2.xlarge')

# spin servers for k8s workers
create_instances(instance_type='t2.large', max_count=2)

# List all instances
for instance in ec2_client.instances.all():
    print(f"Instance ID: {instance.id}")
