#Ex1
import socket

def tcp_connect(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            return s.connect_ex((host, port)) == 0
    except:
        return False

#ex2
import ipaddress

def is_valid_ipv4(text):
    try:
        ipaddress.ip_address(text)
        return True
    except:
        return False
#ex3
def parse_ports(s):
    ports = set()

    for part in s.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            for p in range(start, end + 1):
                ports.add(p)
        else:
            ports.add(int(part))

    return sorted(ports)
#ex4
def scan_ports(host, ports):
    open_ports = []

    for p in ports:
        if tcp_connect(host, p):
            open_ports.append(p)

    return open_ports
#ex5
def grab_banner(host, port):
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)

            if s.connect_ex((host, port)) != 0:
                return None

            data = s.recv(1024)
            if not data:
                return None

            return data.decode("utf-8", errors="replace")

    except:
        return None
    # ex6
def grab_banner(host, port):
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)

            if s.connect_ex((host, port)) != 0:
                return None

            data = s.recv(1024)

            if not data:
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                data = s.recv(1024)

            if not data:
                return None

            return data.decode("utf-8", errors="replace")

    except:
        return None
#ex7
def reverse_dns(ip: str):
    import socket

    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return None
#ex8
import json

def save_results(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
import argparse
#ex9
parser = argparse.ArgumentParser()
parser.add_argument("targets")
parser.add_argument("ports")

args = parser.parse_args()

print("Targets:", args.targets)
print("Ports:", args.ports)
#ex10
import time

def scan_ports(host, ports, delay=0.05):
    open_ports = []

    for p in ports:
        if tcp_connect(host, p):
            open_ports.append(p)
        time.sleep(delay)

    return open_ports
#ex11
COMMON = {
    22: 'SSH',
    80: 'HTTP',
    443: 'HTTPS',
    3306: 'MySQL'
}

def guess_service(port, banner):
    return banner if banner else COMMON.get(port, "inconnu")
#ex12
def print_report(results):
    for ip, entries in results.items():
        print(f"\nHost: {ip}")

        name = reverse_dns(ip)
        if name:
            print(f"Name: {name}")

        for entry in entries:
            port = entry["port"]
            banner = entry.get("banner")

            service = guess_service(port, banner)

        
            if banner:
                banner = banner[:50]

            print(f"  Port {port} → {service}")
            