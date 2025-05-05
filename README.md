
# AWS Security Scanner 🛡️

A lightweight, modular Python tool to scan your AWS environment for common misconfigurations — with a focus on IAM, Security Groups, and S3 buckets. Perfect for indie devs, creatives, or security-minded teams looking for quick visibility into their cloud hygiene.

---

## 🔧 Features

- 🔐 **IAM Scanner**  
  - Detects users with Administrator access  
  - Lists users without MFA  
  - Finds old access keys

- 🌐 **Security Group Scanner**  
  - Flags rules exposing ports to `0.0.0.0/0`

- 🪣 **S3 Scanner**  
  - Detects publicly accessible buckets via ACL or Policy

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/shenrobi/aws-security-scanner.git
cd aws-security-scanner
```

---

## 🧰 Python Environment Setup (Recommended)

To safely install dependencies without affecting your system Python, use a virtual environment:

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# 3. Install required libraries
pip install boto3
```

You’ll now see `(.venv)` in your terminal — that means the environment is active.

> 🧠 **Why This Matters:**  
macOS with Homebrew or Python 3.13+ now restrict system installs due to [PEP 668](https://peps.python.org/pep-0668/). Virtual environments help you avoid breaking system packages and keep your project dependencies clean.

---

### ✅ VS Code Users:
- Open **Command Palette** (`Cmd+Shift+P`)
- Select: `Python: Select Interpreter`
- Choose `.venv/bin/python` to link your project to the environment

---

### 4. Configure your AWS credentials

```bash
aws configure
```

This tool uses your locally stored credentials in `~/.aws/credentials`.

---

## ✅ Run the Scanner

```bash
python main.py
```

This will run all three scanners and print results to the terminal.

---

## 🔐 Required Permissions

Your IAM user or role should have the following minimal permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:List*",
        "ec2:DescribeSecurityGroups",
        "s3:ListAllMyBuckets",
        "s3:GetBucketAcl",
        "s3:GetBucketPolicyStatus"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 📁 Folder Structure

```
aws_sec_scanner/
├── main.py
├── README.md
├── scanners/
│   ├── iam_scanner.py
│   ├── security_group_scanner.py
│   └── s3_scanner.py
└── utils/
    ├── __init__.py
    └── aws_helpers.py
```

---

## 📄 License

MIT – Free for personal and commercial use. Contributions welcome!

---

## ✨ Future Enhancements

- Slack/Email alerts
- Auto-remediation option
- Support for multiple AWS profiles
- Scheduled scans (e.g. cron or GitHub Actions)
- HTML/PDF reporting option
