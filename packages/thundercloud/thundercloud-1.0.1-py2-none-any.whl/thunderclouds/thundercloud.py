import boto3
import botocore
import sys
import paramiko
import time
from botocore.exceptions import ClientError

def command_stdout(client, command):
    _, raw_stdout, _ = client.exec_command(command)
    byte_stdout = raw_stdout.read()
    string_stdout = byte_stdout.decode("ascii")
    return string_stdout

# Transferring a file over and running it 
def put_file(client, local_file_path, remote_file_name):
    sftp = client.open_sftp()
    sftp.put(local_file_path, remote_file_name)
    sftp.close()

def instance_status(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['State']['Name']

def get_instance_ip(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    timeout = 30
    ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')
    while (not ip and timeout > 0):
        time.sleep(1)
        response = ec2.describe_instances(InstanceIds=[instance_id])
        ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')
        timeout -= 1
    if (not ip):
        sys.exit("Timeout Error, couldn't find public IP for this instances!")
    return ip

''' 
Starts ec2 instances with the instance ids found in list instance_ids
instance_ids: list of strings
returns 0 on error, returns dictionary or 1 on success
'''
def start_instance(instance_id):
    if not instance_id:
        print("instance_ids cannot be an empty list!")
        return 0

    ec2 = boto3.client('ec2')
    timeout = 30
    status = instance_status(instance_id)
    while(timeout > 0 and status != 'stopped'):
        if (status == 'running'):
            print("Instance", instance_id ,"already running!")
            return 1
        timeout -= 1
        time.sleep(1)
        status = instance_status(instance_id)
    if (timeout <= 0):
        sys.exit("Timeout Error, could not start the instance")
    
    try:
        start_response = ec2.start_instances(InstanceIds=[instance_id])
    except ClientError as ce:
        print("There was a client error when starting instance!")
        return 0
    time.sleep(10)
    print('Instance', instance_id, 'started!')
    return start_response

''' 
Stops ec2 instances with the instance ids found in list instance_ids
instance_ids: list of strings
returns 0 on error, returns 1 or dictionary on success
'''
def stop_instance(instance_id):
    ec2 = boto3.client('ec2')
    if (instance_status(instance_id) == 'stopped'):
        print("Instance already stopped!")
        return 1
    try:
        stop_response = ec2.stop_instances(InstanceIds=[instance_id])
    except ClientError as ce:
        print("There was a client error when starting instance!")
        return 0
    print('Instance', instance_id, 'stopped!')
    return stop_response

def start_ssh_session(pem_file_path, instance_ip, username):
    key = paramiko.RSAKey.from_private_key_file(pem_file_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    retry = 0
    while(retry < 5):
        try:
            client.connect(hostname=instance_ip, username=username, pkey=key)
            break
        except:
            retry += 1
            time.sleep(2)
    return client
