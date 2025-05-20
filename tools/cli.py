import argparse
from . import aws_ec2_tools

def main():
    parser = argparse.ArgumentParser(description="Tools CLI")
    subparsers = parser.add_subparsers(dest="tool", required=True)

    # AWS subcommand
    aws_ec2_parser = subparsers.add_parser("aws-ec2", help="AWS EC2 tools")
    aws_ec2_parser.add_argument("--action", required=True, choices=["status", "start", "stop"], help="Action to perform")
    aws_ec2_parser.add_argument("--instance-id", required=True, help="EC2 Instance ID")
    aws_ec2_parser.add_argument("--region", default="ap-southeast-1" , help="EC2 Region")

    args = parser.parse_args()

    if args.tool == "aws-ec2":
        aws_ec2_tools.handle_aws(args)

if __name__ == "__main__":
    main()