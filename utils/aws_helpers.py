
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_boto3_client(service_name, region_name=None):
    try:
        if not isinstance(service_name, str) or not service_name.isidentifier():
            raise ValueError("Invalid AWS service name provided.")

        session = boto3.Session()
        client = session.client(service_name, region_name=region_name)
        return client
    except (BotoCoreError, ClientError, ValueError) as e:
        print(f"❌ Error creating boto3 client for {service_name}: {e}")
        return None

def validate_region(region):
    if not isinstance(region, str):
        raise ValueError("Region must be a string.")
    if not region.startswith("us-") and not region.startswith("eu-"):
        raise ValueError("Region format appears invalid.")
    return region
