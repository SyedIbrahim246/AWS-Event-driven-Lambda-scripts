import json
import boto3            #Imports the aws sdk


def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    ##Describe the instances to obtain their  instance id and state. The filter only selects ec2 instances which are currently running.

    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    #Create an empty list for instance ids. The stop_instance command only accepts input from a list.
    Instance_Ids = []

    #This iterates through the reservation and instances list in the response syntax to obtain and add instance Ids to the Instance_Ids list. See describe_instances documentation for more info.
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            Instance_Ids.append(instance['InstanceId'])

    #Iterates through all the instances running and stops them.
    for id in Instance_Ids:
        ec2.stop_instances(InstanceIds=[id])
        print(f"Stopped instance {id}")
    return