import os
import sys
import json
from theme.theme import *

BLOCKED_IPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blocked_ips.json")

"""
Usage - at <project_root>/utilities/:

1. sudo python3 -m utilities.unblock_ip            -> flush all blocked IPs
2. sudo python3 -m utilities.unblock_ip 1.2.3.4    -> unblock a single IP
"""

def load_blocked_ips():
    try:
        with open(BLOCKED_IPS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def clear_blocked_ips_in_table(blocked_ips):
    os.system("pfctl -qt blocked -T flush")
    blocked_ips.clear()
    save_blocked_ips(blocked_ips)


def save_blocked_ips(blocked_ips):
    with open(BLOCKED_IPS_FILE, "w") as f:
        json.dump(blocked_ips, f, indent=2)


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    blocked_ips = load_blocked_ips() # Initialize blocked_ips json records

    if len(sys.argv) > 1:
        ip = sys.argv[1]
        os.system(f"pfctl -qt blocked -T delete {ip}")
        blocked_ips.pop(ip, None)
        save_blocked_ips(blocked_ips)
        print(f"\n{SEPARATOR}\n")
        print(f"{GREEN}MESSAGE: Unblocked {ip}{RESET}")
    else:
        clear_blocked_ips_in_table(blocked_ips)
        print(f"\n{SEPARATOR}\n")
        print(f"{GREEN}MESSAGE:{RESET} Flushed all blocked IPs")

    print(f"\n{SEPARATOR}\n")
    print("Current table contents:")
    os.system("pfctl -qt blocked -T show")
    print(f"\n{SEPARATOR}\n")
