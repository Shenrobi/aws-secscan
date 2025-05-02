
from utils.aws_helpers import get_boto3_client
from botocore.exceptions import ClientError

def check_public_s3_buckets(s3):
    public_buckets = []

    try:
        buckets = s3.list_buckets().get('Buckets', [])
        for bucket in buckets:
            bucket_name = bucket['Name']
            is_flagged = False

            # Check ACLs
            try:
                acl = s3.get_bucket_acl(Bucket=bucket_name)
                for grant in acl.get('Grants', []):
                    grantee = grant.get('Grantee', {})
                    if grantee.get('URI') in [
                        'http://acs.amazonaws.com/groups/global/AllUsers',
                        'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'
                    ]:
                        public_buckets.append({
                            'BucketName': bucket_name,
                            'AccessType': 'Public via ACL'
                        })
                        is_flagged = True
                        break
            except ClientError as e:
                if e.response['Error']['Code'] not in ['AccessDenied', 'NoSuchBucket']:
                    print(f"⚠️ Error checking ACL for {bucket_name}: {e}")

            # Check Bucket Policy if not already flagged
            if not is_flagged:
                try:
                    policy_status = s3.get_bucket_policy_status(Bucket=bucket_name)
                    if policy_status['PolicyStatus']['IsPublic']:
                        public_buckets.append({
                            'BucketName': bucket_name,
                            'AccessType': 'Public via Policy'
                        })
                except ClientError as e:
                    if e.response['Error']['Code'] not in ['AccessDenied', 'NoSuchBucketPolicy']:
                        print(f"⚠️ Error checking policy for {bucket_name}: {e}")

    except ClientError as e:
        print(f"❌ Error listing buckets: {e}")

    return public_buckets

if __name__ == "__main__":
    print("🪣 Running S3 Scanner...")
    s3 = get_boto3_client('s3')

    if s3:
        results = check_public_s3_buckets(s3)
        if not results:
            print("✅ No public S3 buckets found.")
        else:
            for b in results:
                print(f"🛑 {b['BucketName']} is publicly accessible ({b['AccessType']})")
    else:
        print("⚠️ S3 client could not be initialized.")
