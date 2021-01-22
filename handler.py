import json
import os
from io import StringIO

import boto3
import pandas as pd
from botocore.client import Config


def get_s3_resource():
    if os.environ.get('STAGE') in ['local', 'test']:
        return boto3.resource('s3',
                              endpoint_url='http://localhost:9000',
                              aws_access_key_id='minio',
                              aws_secret_access_key='minio123',
                              config=Config(signature_version='s3v4'),
                              region_name='us-east-1')

    return boto3.resource('s3')


def handle_request(event, _):
    path_params = event['pathParameters'] if event.get('pathParameters') else {}
    query_string_params = event['queryStringParameters'] if event.get('queryStringParameters') else {}

    start_from = int(query_string_params.get('start_from', '0'))
    size = int(query_string_params.get('size', '10'))

    order_by = query_string_params.get('order_by', 'risk_score')
    ascending = query_string_params.get('order') == "asc"

    s3_obj = get_s3_resource().Object(bucket_name=os.environ.get('BUCKET_NAME'), key=os.environ.get('OBJECT_KEY'))
    csv_file = StringIO(s3_obj.get()["Body"].read().decode('utf-8'))
    data_frame = pd.read_csv(csv_file, sep=r',(?=\S)', engine='python')

    filtered_df = data_frame.loc[data_frame['host'] == path_params['host']]
    sorted_df = filtered_df.sort_values(by=[order_by], ascending=ascending)
    paginated_df = sorted_df['vulnerability'][start_from:start_from+size]

    response = {
        'order': query_string_params.get('order', 'desc'),
        'order_by': order_by,
        'total': len(sorted_df['vulnerability']),
        'start_from': start_from,
        'size': size,
        'results': paginated_df.values.tolist()
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }

