
from utils.aws_helpers import get_boto3_client
from botocore.exceptions import ClientError

def check_open_security_groups(ec2):
    open_sg_report = []
    try:
        response = ec2.describe_security_groups()
        security_groups = response.get('SecurityGroups', [])

        for sg in security_groups:
            group_id = sg['GroupId']
            group_name = sg.get('GroupName', 'N/A')

            for permission in sg.get('IpPermissions', []):
                ip_ranges = permission.get('IpRanges', [])

                for ip_range in ip_ranges:
                    cidr = ip_range.get('CidrIp', '')
                    if cidr == '0.0.0.0/0':
                        port = permission.get('FromPort', 'All')
                        protocol = permission.get('IpProtocol', 'All')
                        open_sg_report.append({
                            'GroupId': group_id,
                            'GroupName': group_name,
                            'Port': port,
                            'Protocol': protocol,
                            'CIDR': cidr
                        })
    except ClientError as e:
        print(f"❌ Error retrieving security groups: {e}")

    return open_sg_report

if __name__ == "__main__":
    print("🌐 Running Security Group Scanner...")
    ec2 = get_boto3_client('ec2')

    if ec2:
        results = check_open_security_groups(ec2)
        if not results:
            print("✅ No wide-open Security Groups found.")
        else:
            for r in results:
                print(f"🛑 {r['GroupId']} ({r['GroupName']}) allows {r['Protocol']} traffic on port {r['Port']} from {r['CIDR']}")
    else:
        print("⚠️ EC2 client could not be initialized.")
