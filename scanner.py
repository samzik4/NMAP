import socket
import argparse

def scan_tcp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return "ABERTA"
        else:
            return "FECHADA/FILTRADA"
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

def main():
    parser = argparse.ArgumentParser(description="Scanner TCP/UDP Simples")
    parser.add_argument("ips", nargs="+", help="Um ou mais endereços IP")
    parser.add_argument("-p", "--ports", default="1-1024", help="Intervalo de portas (ex: 20-80)")
    parser.add_argument("-t", "--tcp", action="store_true", help="Varredura TCP")
    parser.add_argument("-u", "--udp", action="store_true", help="Varredura UDP")
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))

    for ip in args.ips:
        print(f"\n>>> Escaneando {ip}\n{'='*40}")
        for port in range(start_port, end_port + 1):
            if args.tcp:
                status = scan_tcp(ip, port)
                print(f"[TCP] Porta {port}: {status}")
            if args.udp:
                status = scan_udp(ip, port)
                print(f"[UDP] Porta {port}: {status}")

if __name__ == "__main__":
    main()
