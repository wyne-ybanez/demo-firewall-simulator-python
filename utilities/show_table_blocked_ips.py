import os
import sys
import json
from dos_blocker import load_blocked_ips
from utilities.unblock_ip import save_blocked_ips

"""
Usage - at <project_root>/utilities/:

1. sudo python3 -m utilities.show_table_blocked_ips   -> show all blocked IPs
"""

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    print("\nCurrent table contents:\n")
    blocked_ips = load_blocked_ips()
    os.system("pfctl -qt blocked -T show")
    print("\n")