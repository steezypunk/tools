import os
import boto3
import time

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
                wait_for_state(ec2, instance_id, "running")
                info(ec2, instance_id)
            else:
                print(f"Instance {instance_id} is not stopped (current state: {state})")
        elif args.action == "stop":
            response = ec2.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            if state != "stopped":
                ec2.stop_instances(InstanceIds=[instance_id])
                print(f"Stopping instance {instance_id}")
                wait_for_state(ec2, instance_id, "stopped")
            else:
                print(f"Instance {instance_id} is already stopped")
        else:
            print(f"Unknown action: {args.action}")

def wait_for_state(ec2, instance_id, target_state):
    print(f"Waiting for instance {instance_id} to reach '{target_state}' state", end="", flush=True)
    while True:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
        if state == target_state:
            print(" done.")
            break
        print(".", end="", flush=True)
        time.sleep(3)

def info(ec2, instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response["Reservations"][0]["Instances"][0]
    state = instance["State"]["Name"]
    public_ip = instance.get("PublicIpAddress", "N/A")
    hostname = instance.get("PrivateDnsName", "N/A")
    public_dns = instance.get("PublicDnsName", "N/A")
    print(f"State: {state}")
    print(f"Public IPv4: {public_ip}")
    print(f"Hostname: {hostname}")
    print(f"Public IPv4 DNS: {public_dns}")