from fastapi import FastAPI
from hosts_calc import get_hosts, get_network_info

app = FastAPI()


@app.get("/hosts")
def hosts_default():
    hosts = get_hosts("192.168.10.0/26")
    return {"hosts": hosts}


@app.get("/count")
def count_hosts(network: str):
    info = get_network_info(network)
    return {
        "network": info["network"],
        "broadcast": info["broadcast"],
        "netmask": info["netmask"],
        "usable_hosts": info["usable_hosts"]
    }

@app.get("/network_info")
def network_info(network: str):
    return get_network_info(network)