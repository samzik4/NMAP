import socket

def scan_tcp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((ip, port))
        return "ABERTA" if result == 0 else "FECHADA/FILTRADA"
    except Exception:
        return "ERRO"
    finally:
        sock.close()

def scan_udp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        sock.sendto(b"", (ip, port))
        sock.recvfrom(1024)
        return "ABERTA"
    except socket.timeout:
        return "ABERTA/FILTRADA"
    except Exception:
        return "FECHADA"
    finally:
        sock.close()

# ================= Interface no terminal =================
print("=== MINI SCANNER TCP/UDP ===\n")

ip = input("Digite o endereco IP: ").strip()
ports = input("Digite o intervalo de portas (ex: 20-80): ").strip()

try:
    start_port, end_port = map(int, ports.split("-"))
except:
    print("Intervalo de portas invalido!")
    exit()

tcp_choice = input("Deseja varredura TCP? (s/n): ").strip().lower() == "s"
udp_choice = input("Deseja varredura UDP? (s/n): ").strip().lower() == "s"

if not (tcp_choice or udp_choice):
    print("Selecione pelo menos TCP ou UDP!")
    exit()

print(f"\n>>> Escaneando {ip}\n{'='*40}")

for port in range(start_port, end_port + 1):
    if tcp_choice:
        status = scan_tcp(ip, port)
        print(f"[TCP] Porta {port}: {status}")
    if udp_choice:
        status = scan_udp(ip, port)
        print(f"[UDP] Porta {port}: {status}")
