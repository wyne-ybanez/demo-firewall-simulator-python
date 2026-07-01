import os
import sys

"""
Usage - at <project_root>/utilities/:

1. sudo python3 show-blocked-ips.py   -> show all blocked IPs
"""

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    print("\nCurrent table contents:\n")
    os.system("pfctl -qt blocked -T show")
    print("\n")