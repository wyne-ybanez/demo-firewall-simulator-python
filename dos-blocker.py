import os
import sys
import time

from collections import defaultdict # for storing and managing packet counts for each source IP
from scapy.all import sniff, IP # for packet sniffing and IP address manipulation

# Threshold for a sample DoS attack
THRESHOLD = 40
print(f"THRESHOLD: {THRESHOLD}")

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

                print(f"Blocking IP: {ip}, packet rate: {packet_rate}")

                # LINUX SERVERS
                # os.system(f"iptables -A INPUT -s {ip} -j DROP")

                # MAC SERVERS
                os.system(f"echo 'block in from {ip} to any' | pfctl -ef -")

                blocked_ips.add(ip)

        packet_count.clear()

        start_time[0] = current_time


if __name__ == "__main__":

    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    packet_count = defaultdict(int) # assigns a default value of 0 for any new IP address encountered

    start_time = [time.time()]

    blocked_ips = set() # to keep track of already blocked IPs, initially an empty object

    # MAC SERVERS: Enable pfctl first
    os.system("pfctl -e 2>/dev/null")

    print("Monitoring network traffic...")

    sniff(filter="ip", prn=packet_callback) # sniffing for IP packets and calling `packet_callback` for each captured packet