# 🛡️ DNS-Spoofer-Python-FireFly

A simple DNS Spoofer written in Python.  
This project demonstrates how DNS spoofing works in a controlled environment for **educational and ethical hacking purposes only**.

---

## ⚙️ Setup Instructions

### 1. Download the Files
Clone or download this repository to your local machine.

```bash
git clone https://github.com/HadiMuhammed/DNS-Spoofer-Python-FireFly.git


1. Download the Files
Clone or download this repository to your local machine:

2. Get Your IP Address (ipconfig)
Open Command Prompt and run:
ipconfig

Ethernet adapter Local Area Connection:

   IPv4 Address. . . . . . . . . . . : 192.168.20.3
   IPv6 Address. . . . . . . . . . . : 2403:a080:d:89be:caac:a86:fc0:6885

3. Configure hosts.txt
Edit the hosts.txt file and add entries in the following format:
wxx.example.cmm ,192.168.20.3 ,2403:a080:d:89be:caac:a86:fc0:6885


wxx.example.cmm → The website you want to spoof

192.168.20.3 → Your IPv4 address

2403:a080:d:89be:caac:a86:fc0:6885 → Your IPv6 address from ipconfig


4. Run the Spoofer
Open PowerShell as Administrator and run:

command to activate env: ./firefly/Script/activate

python dns_spoofer.py

now run the link 
http://wxx.example.cmm 
(donot add https://, this tool only works on http://)
