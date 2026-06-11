import json
import boto3


def lambda_handler(event, context):
    sns_client = boto3.client('sns')

    # Replace with your SNS Topic ARN
    sns_topic_arn = 'arn:aws:sns:region:account-id:topic-name'

    records = event.get('Records', [])

    if not records:
        return {
            "statusCode": 400,
            "body": "No S3 event records."
        }

    try:
        s3_info = records[0]['s3']
        bucket = s3_info['bucket']['name']
        file_key = s3_info['object']['key']

        message = f"""
Lambda executed successfully!

File: {file_key}
Bucket: {bucket}
"""

        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="S3 File Upload Notification",
            Message=message
        )

        return {
            'statusCode': 200,
            'body': json.dumps(
                f'Notification sent successfully for file {file_key}.'
            )
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(
                f'Error sending notification: {str(e)}'
            )
        }