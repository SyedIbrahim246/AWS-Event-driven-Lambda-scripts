#Create a Lambda function to tag EC2 Instances with the name of the owner
#Link an EventBridge to a Lambda function
#Use CloudTrail to log the instances when Lambda function is triggered

import json
import boto3            #Imports the aws sdk

ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    print(event)

    user = event['detail']['userIdentity']['userName']      #the event is accessed from cloudtrail logs. The json file can be formatted using a tool online for easier reading

    instanceId = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']

    ec2.create_tags(                                        #The client name is defined in line 8. The standard client.function needs to be modified from the boto3 documentation

        Resources=[
            instanceId,
        ],
        Tags=[
            {
                'Key': 'Owner',
                'Value': user   },
        ]
    )

    return


import json
import boto3
import sys

ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    print(event)

    user = event['detail']['userIdentity']['userName']

    instanceId = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']

    for tag in event['detail']['requestParameters']['tagSpecificationSet']['items'][0]['tags']:
        if tag['key'] == "Owner" or tag['key'] == "owner":
            print("Instance already has an owner tag")
            sys.exit(0)

    ec2.create_tags(

        Resources=[
            instanceId,
        ],
        Tags=[
            {
                'Key': 'Owner',
                'Value': user},
        ]
    )

    print("Owner tag" + user + "has been added")

    return


