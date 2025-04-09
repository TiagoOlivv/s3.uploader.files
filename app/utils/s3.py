import boto3
from botocore.exceptions import ClientError

def create_s3_client(region, access_key, secret_key):
    try:
        return boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    except Exception as e:
        raise Exception(f"Failed to create S3 client: {e}")

def ensure_bucket_exists(s3, bucket_name, region):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        else:
            raise Exception(f"Bucket check error: {e}")
