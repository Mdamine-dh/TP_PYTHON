import ipaddress

def get_hosts(network_cidr="192.168.10.0/26"):
    network = ipaddress.ip_network(network_cidr)
    hosts = [str(ip) for ip in network.hosts()]
    
    
    with open("hosts.txt", "w") as f:
        for host in hosts:
            f.write(host + "\n")
    
    return hosts

def get_network_info(network_cidr):
    network = ipaddress.ip_network(network_cidr)
    info = {
        "network": str(network.network_address),
        "broadcast": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "usable_hosts": len(list(network.hosts())),
        "hosts": [str(ip) for ip in network.hosts()]
    }
    return info