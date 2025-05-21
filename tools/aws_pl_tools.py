import sys
import boto3
import argparse
import requests

def validate_tool(tool):
    return tool == "aws-pl"

def fetch_prefix_list(client, prefix_list_id):
    try:
        resp = client.describe_managed_prefix_lists(PrefixListIds=[prefix_list_id])
        return resp['PrefixLists'][0]
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def fetch_prefix_list_entries(client, prefix_list_id):
    try:
        resp = client.get_managed_prefix_list_entries(PrefixListId=prefix_list_id)
        return resp['Entries']
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def prefix_list_contains_ip(entries, ip):
    return any(entry['Cidr'] == ip for entry in entries)

def get_my_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        sys.exit(1)

def add_ip(client, prefix_list_id, ip):
    entries = fetch_prefix_list_entries(client, prefix_list_id)
    if prefix_list_contains_ip(entries, ip):
        print(f"{ip} already exists in {prefix_list_id}, skipping add.")
        return
    prefix_list = fetch_prefix_list(client, prefix_list_id)
    try:
        client.modify_managed_prefix_list(
            PrefixListId=prefix_list_id,
            CurrentVersion=prefix_list['Version'],
            AddEntries=[{'Cidr': ip, 'Description': 'Added by aws_pl_tools'}],
            RemoveEntries=[]
        )
        print(f"Added {ip} to {prefix_list_id}.")
    except Exception as e:
        print(f"Error adding IP: {e}")

def remove_ip(client, prefix_list_id, ip):
    entries = fetch_prefix_list_entries(client, prefix_list_id)
    if not prefix_list_contains_ip(entries, ip):
        print(f"{ip} not found in {prefix_list_id}, skipping remove.")
        return
    prefix_list = fetch_prefix_list(client, prefix_list_id)
    try:
        client.modify_managed_prefix_list(
            PrefixListId=prefix_list_id,
            CurrentVersion=prefix_list['Version'],
            AddEntries=[],
            RemoveEntries=[{'Cidr': ip}]
        )
        print(f"Removed {ip} from {prefix_list_id}.")
    except Exception as e:
        print(f"Error removing IP: {e}")

def main():
    parser = argparse.ArgumentParser(description="AWS Prefix List Tools")
    parser.add_argument("--tool", required=True, help="Tool name, must be 'aws-pl'")
    parser.add_argument("--action", required=True, choices=["add", "remove"], help="Action to perform")
    parser.add_argument("--prefix-list-id", required=True, help="Prefix List ID")
    parser.add_argument("--ip", required=True, help="IP/CIDR to add or remove")
    args = parser.parse_args()

    if not validate_tool(args.tool):
        print("Invalid tool. Only 'aws-pl' is supported.")
        sys.exit(1)

    client = boto3.client('ec2')

    ip = args.ip
    entries = fetch_prefix_list_entries(client, args.prefix_list_id)
    if args.action == "add":
        if not prefix_list_contains_ip(entries, ip):
            print(f"{ip} does not exist in {args.prefix_list_id}. Checking your current outgoing IP...")
            my_ip = get_my_public_ip()
            print(f"Your current outgoing IP is: {my_ip}")
        add_ip(client, args.prefix_list_id, ip)
    elif args.action == "remove":
        remove_ip(client, args.prefix_list_id, ip)
    else:
        print("Invalid action.")
        sys.exit(1)

if __name__ == "__main__":
    main()