import socket 
from IPy import IP

open_ports = []
open_port_banners = []

def scan(targets_list, ports):
    open_ports.clear()
    open_port_banners.clear()
    for target in targets_list:
        converted_ip = check_ip(target)
        print("\nScanning target: " + str(converted_ip))
        scan_port(converted_ip, ports)

def check_ip(ip):
    try:
        IP(ip)
        return ip
    except Exception:
        return socket.gethostbyname(ip)

def get_banner(sock):
    try:
        return sock.recv(1024).decode('utf-8', errors='ignore')
    except Exception:
        return None

def scan_port(ipaddress, ports):
    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((ipaddress, port))
            banner = get_banner(sock)
            open_ports.append(port)
            open_port_banners.append(banner if banner else 'No banner')
        except Exception as e:
            print(f"Could not connect to {ipaddress}:{port} - {e}")
        finally:
            sock.close()

targets_list = []
ports = []

targets = input("Enter target/targets to scan (split multiple targets with ',') : ")

if ',' in targets:
    targets_list = [ip_add.strip() for ip_add in targets.split(",")]
else:
    targets_list.append(targets.strip())

port_choice = input("Please enter 'all_ports' to scan all ports, or specify individual ports:\n"
                    "(Separate multiple ports with commas, or type 0 to finish entering): ")

if port_choice.lower() == "all_ports":
    ports = list(range(1, 65536))  
else:
    while port_choice != '0':
        try:
            number = int(port_choice)
            if number < 1 or number > 65535:
                print("Please enter a number between 1 and 65535")
            else:
                ports.append(number)
        except ValueError:
            print("Invalid input. Please enter a port or 'all_ports' to scan all ports.")
        port_choice = input("Enter another port, or type 0 to finish: ")

scan(targets_list, ports)

if open_ports:
    print("Open ports and banners: ")
    for port, banner in zip(open_ports, open_port_banners):
        print(f"Port: {port}, Banner: {banner if banner else 'No banner'}")
else:
    print("No open ports found.")
