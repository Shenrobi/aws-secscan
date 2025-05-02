
from scanners.iam_scanner import list_admin_users, list_users_without_mfa, list_old_access_keys
from scanners.security_group_scanner import check_open_security_groups
from scanners.s3_scanner import check_public_s3_buckets
from utils.aws_helpers import get_boto3_client

def run_iam_scanner():
    print("\n🔐 IAM Scanner Results")
    iam = get_boto3_client('iam')
    if not iam:
        print("⚠️ IAM client could not be initialized.")
        return

    admin_users = list_admin_users(iam)
    print(f"🛑 Admin Users: {admin_users or 'None'}")

    no_mfa = list_users_without_mfa(iam)
    print(f"🔓 Users without MFA: {no_mfa or 'None'}")

    old_keys = list_old_access_keys(iam)
    print("📅 Access Keys older than 90 days:")
    for key in old_keys:
        print(f" - {key['UserName']} | {key['AccessKeyId']} | {key['AgeDays']} days old")

def run_sg_scanner():
    print("\n🌐 Security Group Scanner Results")
    ec2 = get_boto3_client('ec2')
    if not ec2:
        print("⚠️ EC2 client could not be initialized.")
        return

    results = check_open_security_groups(ec2)
    if not results:
        print("✅ No wide-open Security Groups found.")
    else:
        for r in results:
            print(f"🛑 {r['GroupId']} ({r['GroupName']}) allows {r['Protocol']} traffic on port {r['Port']} from {r['CIDR']}")

def run_s3_scanner():
    print("\n🪣 S3 Scanner Results")
    s3 = get_boto3_client('s3')
    if not s3:
        print("⚠️ S3 client could not be initialized.")
        return

    results = check_public_s3_buckets(s3)
    if not results:
        print("✅ No public S3 buckets found.")
    else:
        for b in results:
            print(f"🛑 {b['BucketName']} is publicly accessible ({b['AccessType']})")

if __name__ == "__main__":
    print("🚨 AWS Security Scanner – Starting Full Scan...")
    run_iam_scanner()
    run_sg_scanner()
    run_s3_scanner()
    print("\n✅ Scan complete.")
