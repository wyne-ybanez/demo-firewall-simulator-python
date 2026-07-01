# Python Firewall Simulator

Script simulates a simple Firewall and Dos Blocker.
Project was built on personal Mac machine hence, multiple Mac commands are in the README.

**To Do:**

- build DoS tester / flooder to test if this firewall sim works as intended. [ ]

&nbsp;

## Requirements

You'll need to install project requirements. Run: `pip install -r requirements.txt`

&nbsp;

## How to run

1. **Firewall Rules**
Run: `sudo python3 firewall_rules.py`

2. **DoS Blocker**
Run: `sudo python3 dos_blocker.py`

&nbsp;

## Utility Scripts

1. **Network Scanner (MacOS)**
Run at root level: `python3 -m utilities.macos_net_scan`

2. **Unblock IPs (MacOs)**
- Run at root level: `sudo python3 -m utilities.unblock_ip` - Unblocks all IPs from table
- Run at root level: `sudo python3 -m utilities.unblock_ip 1.2.3.4` - Unblocks a specific IP from table

3. **Show Blocked IPs Table (MacOS)**
Run at root level: `sudo python3 -m utilities.show_table_blocked_ips` - Displays all blocked IP addresses on your custom table

#### Check your IP tables for any blocked IP addresses.

- Linux Server - in your terminal run: `sudo iptables -L INPUT -n`

- Mac Server - in your terminal run:
    - `sudo pfctl -sr` - show the main ruleset
    - `sudo pfctl -sA` — lists all anchor names pf currently knows about, useful to confirm `dos_blocker` shows up at all.

Both these commands lists your active rules, including any IPs your script blocked.

&nbsp;

#### MAC terminal commands for network information

- check your interfaces and IP address: `ifconfig`

- check your own IP address: `ipconfig getifaddr ${interface-you're-on e.g. en0}`

- check what interface your machine is on and who's on your network: `arp -a`

- I made a network scanner utility script for MacOS devices, which does all of the above and displays it into the terminal in a visually better way. Run at root level: `python3 -m utilities.macos_net_scan`

&nbsp;

#### Caution

1. For Mac machines you may encounter the response - this is an expected output and you can just ignore it:

```
No ALTQ support in kernel
ALTQ related functions disabled
```

2. For this project to work it is assumed you do not manually edit your `blocked_ips.json`.

&nbsp;

## Tech

Python version = 3.14.4
