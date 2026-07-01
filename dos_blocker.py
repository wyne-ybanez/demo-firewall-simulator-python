import os
import sys
import time
import json
from theme.theme import *

from collections import defaultdict # for storing and managing packet counts for each source IP
from scapy.all import sniff, IP # for packet sniffing and IP address manipulation


THRESHOLD = 40 # Threshold for a sample DoS attack
ANCHOR_NAME = "dos_blocker"
BLOCKED_IPS_FILE = "blocked_ips.json"


def setup_pf():
    """
    MacOS Servers:

    - Creates a table for blocked IPs, enables pf
    - Loads a single block rule referencing that table into our own anchor.
    """
    os.system("pfctl -e 2>/dev/null")
    os.system(f"echo 'block in from <blocked> to any' | pfctl -a {ANCHOR_NAME} -qf -")
    print(f"{GREEN}ANCHOR:{RESET} '{ANCHOR_NAME}' created with table <blocked>\n")


def load_blocked_ips():
    """
    Loads blocked IPs from the JSON file on disk.

    Falls back to an empty dict if the file doesn't exist yet.
    Also re-adds any persisted IPs into the pf table in case pf was reset.
    """
    try:
        with open(BLOCKED_IPS_FILE) as f:
            data = json.load(f)

            for ip in data:
                os.system(f"pfctl -qt blocked -T add {ip} 2>/dev/null")
            print(f"{YELLOW}STATUS:{RESET} Loaded {len(data)} blocked IP(s) from {BLOCKED_IPS_FILE}")
            return data
    except FileNotFoundError:
        return {}


def save_blocked_ips(blocked_ips):
    """
    Saves the current blocked IPs dict to a JSON file.
    """
    with open(BLOCKED_IPS_FILE, "w") as f:
        json.dump(blocked_ips, f, indent=2)


def packet_callback(packet):
    """
    Calculates the packet rate for each source IP and blocks IPs that exceed the threshold.
    """
    src_ip_address = packet[IP].src
    packet_count[src_ip_address] += 1
    current_time = time.time()
    time_interval = current_time - start_time[0]

    if time_interval >= 1:
        for ip, count in packet_count.items():
            packet_rate = count / time_interval
            print(f"IP: {ip}, Packet rate: {packet_rate}")

            # If the packet rate exceeds the threshold and the IP is not already blocked, block it using iptables
            if packet_rate > THRESHOLD and ip not in blocked_ips:
                print(f"{RED}BLOCK - IP: {ip}, Packet rate: {packet_rate}{RESET}")

                # LINUX SERVERS
                # os.system(f"iptables -A INPUT -s {ip} -j DROP")

                # MAC SERVERS
                os.system(f"pfctl -qt blocked -T add {ip}")
                blocked_ips[ip] = {
                    "blocked_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                    "packet_rate": round(packet_rate, 3)
                }
                save_blocked_ips(blocked_ips)

        packet_count.clear()
        start_time[0] = current_time


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    # Initialize packet count dictionary, start time, and blocked IPs set
    packet_count = defaultdict(int)
    start_time = [time.time()]

    print(f"\n{SEPARATOR}\n")
    print(f"{GREEN}THRESHOLD:{RESET} {THRESHOLD} Packets per second")
    print(f"\n{SEPARATOR}\n")
    setup_pf()
    print(f"\n{SEPARATOR}\n")
    blocked_ips = load_blocked_ips()
    print(f"\n{SEPARATOR}\n")

    if blocked_ips:
        print(f"{CYAN}MESSAGE:{RESET} Loaded {len(blocked_ips)} already-blocked IP(s) from previous run. \n\n{blocked_ips}")
        print(f"\n{SEPARATOR}\n")

    print("Monitoring network traffic...\n")
    sniff(filter="ip", prn=packet_callback) # sniffing for IP packets and calling `packet_callback` for each captured packet
