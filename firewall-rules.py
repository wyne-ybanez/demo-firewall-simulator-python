import random
from theme.theme import *

ACTION_ALLOW = f"{GREEN}ALLOW{RESET}"
ACTION_BLOCK = f"{RED}BLOCK{RESET}"


def generate_random_ip(max_octet=255):
    """Generate a random IP address."""
    return f"192.168.1.{random.randint(0, max_octet)}"


def check_firewall_rules(ip_address, firewall_rules):
    """Check if the IP address matches any firewall rule and return the action."""
    for rule_ip, action in firewall_rules.items():

        if ip_address == rule_ip:
            return action

    return ACTION_ALLOW  # Default action if no rule matches


def main():
    """
    Define the firewall rules (key: IP address, value: action)
    """

    # block these IP addresses, allow the rest
    firewall_rules = {
        "192.168.1.1": ACTION_BLOCK,
        "192.168.1.4": ACTION_BLOCK,
        "192.168.1.9": ACTION_BLOCK,
        "192.168.1.13": ACTION_BLOCK,
        "192.168.1.16": ACTION_BLOCK,
        "192.168.1.19": ACTION_BLOCK,
        "192.168.1.203": ACTION_BLOCK
    }

    # Simulate network traffic
    for i in range(16):
        ip_address = generate_random_ip()
        action = check_firewall_rules(ip_address, firewall_rules)
        random_number_id = random.randint(0, 999999999) # service a unique ID for each request

        print(f"{i+1}. {action} - IP: {ip_address}, ID: {random_number_id}")

if __name__ == "__main__":
    main()

