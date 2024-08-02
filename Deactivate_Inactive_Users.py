#Create a Lambda function that runs on a schedule of every 24 hours, and looks at the existing IAM users gets their last user activity and access key age. If last activity is more than 30 days then revoke the console access
# and if access key age is more than 90 days then deactivate the key.

import boto3
import json
from datetime import datetime, timedelta


def lambda_handler(event, context):
    iam = boto3.client('iam')
    current_date = datetime.now()
    users = iam.list_users()['Users']

    for user in users:
        username = user['Username']

        access_advisor_data = iam.get_access_advisor_usage(Username=username)
        last_accessed_timestamp = access_advisor_data['ServicesLastAccessed'][0]['LastAuthenticated']
        last_accessed_date = datetime.utcfromtimestamp(last_accessed_timestamp)
        days_difference = (current_date - last_accessed_date).days

        if days_difference > 30:
            iam.delete_login_profile(UserName=username)

        access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']

        for key in access_keys:
            access_key_id = key['AccessKeyId']
            create_date = key['CreateDate']

            key_age = (current_date - create_date).days

            if key_age > 90:
                iam.update_access_key(UserName=username, AccessKeyId=access_key_id, Status='Inactive')

    return