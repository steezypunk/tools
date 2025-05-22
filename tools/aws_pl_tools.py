import sys
import requests

def handle(args, client):
    if validate_tool(args.tool):
        ip = args.ip
        if not ip:
            print(f"{ip} does not exist in {args.prefix_list_id}. Checking your current outgoing IP...")
            ip = get_my_public_ip()

        ip = normalize_ip_to_cidr(ip)
        print(f"Your current outgoing IP is: {ip}")
            
        entries = fetch_prefix_list_entries(client, args.prefix_list_id)
        if args.action == "add":
            if not prefix_list_contains_ip(entries, ip):
                add_ip(client, args.prefix_list_id, ip)
            else:
                print(f"Won't add ip, exist")
        elif args.action == "remove":
            if prefix_list_contains_ip(entries, ip):
                remove_ip(client, args.prefix_list_id, ip)
            else:
                print(f"Won't del ip, not exist")
        elif args.action == "list":
            entries = fetch_prefix_list_entries(client, args.prefix_list_id)
            if not entries:
                print("Prefix list is empty.")
            else:
                for entry in entries:
                    print(entry)
        else:
            print(f"Unknown action: {args.action}")

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

def normalize_ip_to_cidr(ip):
    # Check if the input is already in CIDR format
    if '/' in ip:
        return ip
    # Otherwise, append /32 to denote a single IP address in CIDR
    return f"{ip}/32"

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