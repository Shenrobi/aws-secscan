from utils.aws_helpers import get_boto3_client
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def list_admin_users(iam):
    try:
        users = iam.list_users()['Users']
        admin_users = []

        for user in users:
            username = user['UserName']
            policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
            for policy in policies:
                if policy['PolicyName'] == 'AdministratorAccess':
                    admin_users.append(username)
                    break

        return admin_users
    except ClientError as e:
        print(f"❌ Error listing admin users: {e}")
        return []

def list_users_without_mfa(iam):
    try:
        users = iam.list_users()['Users']
        users_without_mfa = []

        for user in users:
            mfa = iam.list_mfa_devices(UserName=user['UserName'])['MFADevices']
            if not mfa:
                users_without_mfa.append(user['UserName'])

        return users_without_mfa
    except ClientError as e:
        print(f"❌ Error listing MFA devices: {e}")
        return []

def list_old_access_keys(iam, days_threshold=90):
    try:
        users = iam.list_users()['Users']
        old_keys = []

        for user in users:
            keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
            for key in keys:
                age = (datetime.now(timezone.utc) - key['CreateDate']).days
                if age > days_threshold:
                    old_keys.append({
                        'UserName': user['UserName'],
                        'AccessKeyId': key['AccessKeyId'],
                        'AgeDays': age
                    })

        return old_keys
    except ClientError as e:
        print(f"❌ Error listing old access keys: {e}")
        return []

if __name__ == "__main__":
    print("🔐 Running IAM Scanner...\n")
    iam = get_boto3_client('iam')

    if iam:
        admin_users = list_admin_users(iam)
        print(f"🛑 Admin Users: {admin_users or 'None'}")

        no_mfa = list_users_without_mfa(iam)
        print(f"🔓 Users without MFA: {no_mfa or 'None'}")

        old_keys = list_old_access_keys(iam)
        print("📅 Access Keys older than 90 days:")
        if old_keys:
            for key in old_keys:
                print(f" - {key['UserName']} | {key['AccessKeyId']} | {key['AgeDays']} days old")
        else:
            print("✅ No access keys older than 90 days found.")
    else:
        print("⚠️ IAM client could not be initialized.")
