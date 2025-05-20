import os
import boto3

def handle_aws(args):
    if args.tool == "aws-ec2":
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_ACCESS_KEY_SECRET")

        ec2 = boto3.client(
            "ec2",
            region_name=args.region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        instance_id = args.instance_id

        if args.action == "status":
            response = ec2.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            print(f"Instance {instance_id} status: {state}")
        elif args.action == "start":
            response = ec2.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            if state == "stopped":
                ec2.start_instances(InstanceIds=[instance_id])
                print(f"Starting instance {instance_id}")
            else:
                print(f"Instance {instance_id} is not stopped (current state: {state})")
        elif args.action == "stop":
            response = ec2.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            if state != "stopped":
                ec2.stop_instances(InstanceIds=[instance_id])
                print(f"Stopping instance {instance_id}")
            else:
                print(f"Instance {instance_id} is already stopped")
        else:
            print(f"Unknown action: {args.action}")