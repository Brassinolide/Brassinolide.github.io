from scapy.all import *
import socket

SYN = 0x02
RST = 0x04
ACK = 0x10
SYN_ACK = 0x12
RST_ACK = 0x14

def syn_scan(ip:str, port:int, rst:bool = True, timeout:int = 5) -> bool:
    ip_pkt = IP(dst = ip)
    tcp_pkt = TCP(sport = RandShort()._fix(), dport = port, flags = "S")
    response = sr1(ip_pkt / tcp_pkt, timeout = timeout, verbose = 0)
    if response and response.haslayer(TCP):
        flags = response.getlayer(TCP).flags
        if flags == SYN_ACK:
            if rst:
                send(ip_pkt / TCP(sport = tcp_pkt.sport, dport = port, flags = "RA", seq = response.ack, ack = response.seq + 1), verbose = 0)
            return True
        elif flags == RST_ACK:
            return False
        else:
            raise RuntimeError(f"{port} 未知flags：{flags}")
    else:
        raise RuntimeError(f"{port} 服务器无响应")

def null_scan(ip:str, port:int, timeout:int = 5) -> bool:
    ip_pkt = IP(dst = ip)
    tcp_pkt = TCP(sport = RandShort()._fix(), dport = port, flags = 0)
    response = sr1(ip_pkt / tcp_pkt, timeout = timeout, verbose = 0)
    if response is None:
        return True
    elif response.haslayer(TCP):
        if response.getlayer(TCP).flags == RST_ACK:
            return False
        else:
            raise RuntimeError(f"未知flags：{flags}")

def connect_scan(ip:str, port:int, timeout:int = 5) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))
        except (socket.timeout, socket.error):
            return False
        return True


for i in [21,22,80,443,8889,39001]:
    try:
        if syn_scan("192.168.0.1", i):
            print(f"{i} 开放")
        else:
            print(f"{i} 关闭")
    except RuntimeError as e:
        print(e)
        