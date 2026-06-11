import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('S3Uploads')


def lambda_handler(event, context):
    records = event.get('Records', [])

    if not records:
        return {
            "statusCode": 400,
            "body": "No records found."
        }

    try:
        s3_info = records[0]['s3']
        bucket = s3_info['bucket']['name']
        file_key = s3_info['object']['key']
        size = s3_info['object'].get('size', 0)
        timestamp = int(time.time())

        # Insert metadata into DynamoDB
        table.put_item(
            Item={
                'FileName': file_key,
                'Bucket': bucket,
                'Size': size,
                'Timestamp': timestamp
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(
                f"File '{file_key}' metadata inserted into DynamoDB."
            )
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(
                f"Error processing record: {str(e)}"
            )
        }