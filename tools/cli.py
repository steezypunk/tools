import argparse
import boto3
import os
from . import aws_ec2_tools
from . import aws_pl_tools

def main():
    parser = argparse.ArgumentParser(description="Tools CLI")
    subparsers = parser.add_subparsers(dest="tool", required=True)
    parser.add_argument("--region", default="ap-southeast-1" , help="EC2 Region")

    # AWS subcommand
    aws_ec2_parser = subparsers.add_parser("aws-ec2", help="AWS EC2 tools")

    aws_ec2_parser.add_argument("--action", required=True, choices=["status", "start", "stop"], help="Action to perform")
    aws_ec2_parser.add_argument("--instance-id", default="i-0169a3ef25e0aa69a", help="EC2 Instance ID")

    aws_pl_parser = subparsers.add_parser("aws-pl", help="AWS Prefix List tools")
    aws_pl_parser.add_argument("--action", required=True, choices=["add", "remove", "list"], help="Action to perform")
    aws_pl_parser.add_argument("--prefix-list-id", default="pl-0088e1d4399b9ad17", help="Prefix List ID")
    aws_pl_parser.add_argument("--ip", help="IP/CIDR to add or remove")

    args = parser.parse_args()

    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_ACCESS_KEY_SECRET")

    client = boto3.client(
        "ec2",
        region_name=args.region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    if args.tool == "aws-ec2":
        aws_ec2_tools.handle(args, client)
    elif args.tool == "aws-pl":
        aws_pl_tools.handle(args, client)

if __name__ == "__main__":
    main()