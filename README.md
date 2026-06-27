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

1. **Firewall Simulator Starter**

Run: `sudo python3 firewall-simulator.py`

2. **DoS Blocker**

Run: `sudo python3 dos-blocker.py`

#### Check your IP tables for any blocked IP addresses.

- Linux Server - in your terminal run: `sudo iptables -L INPUT -n`

- Mac Server - in your terminal run: `sudo pfctl -sr`

Both these commands lists your active rules, including any IPs your script blocked.

&nbsp;

#### MAC terminal commands for network information

- check your interfaces and IP address: `ifconfig`

- check your own IP address: `ipconfig getifaddr ${interface-you're-on e.g. en0}`

- check what interface your machine is on and who's on your network: `arp -a`


&nbsp;

#### Caution

For Mac machines you may encounter the response:

```
No ALTQ support in kernel
ALTQ related functions disabled
scrub-anchor "com.apple/*" all fragment reassemble
anchor "com.apple/*" all
```

&nbsp;

## Tech

Python version = 3.14.4