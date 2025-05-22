import time

def handle(args, client):
    if args.tool == "aws-ec2":
        instance_id = args.instance_id

        if args.action == "status":
            response = client.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            print(f"Instance {instance_id} status: {state}")
        elif args.action == "start":
            response = client.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            if state == "stopped":
                client.start_instances(InstanceIds=[instance_id])
                print(f"Starting instance {instance_id}")
                wait_for_state(client, instance_id, "running")
                info(client, instance_id)
            else:
                print(f"Instance {instance_id} is not stopped (current state: {state})")
        elif args.action == "stop":
            response = client.describe_instances(InstanceIds=[instance_id])
            state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
            if state != "stopped":
                client.stop_instances(InstanceIds=[instance_id])
                print(f"Stopping instance {instance_id}")
                wait_for_state(client, instance_id, "stopped")
            else:
                print(f"Instance {instance_id} is already stopped")
        else:
            print(f"Unknown action: {args.action}")

def wait_for_state(client, instance_id, target_state):
    print(f"Waiting for instance {instance_id} to reach '{target_state}' state", end="", flush=True)
    while True:
        response = client.describe_instances(InstanceIds=[instance_id])
        state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
        if state == target_state:
            print(" done.")
            break
        print(".", end="", flush=True)
        time.sleep(3)

def info(client, instance_id):
    response = client.describe_instances(InstanceIds=[instance_id])
    instance = response["Reservations"][0]["Instances"][0]
    state = instance["State"]["Name"]
    public_ip = instance.get("PublicIpAddress", "N/A")
    hostname = instance.get("PrivateDnsName", "N/A")
    public_dns = instance.get("PublicDnsName", "N/A")
    print(f"State: {state}")
    print(f"Public IPv4: {public_ip}")
    print(f"Hostname: {hostname}")
    print(f"Public IPv4 DNS: {public_dns}")