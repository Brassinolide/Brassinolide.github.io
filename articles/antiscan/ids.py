from scapy.all import *
import ipaddress

PORT_SCAN_THRESHOLD = 4
record = {}
def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport

        if ipaddress.IPv4Address(src_ip).is_global:
            if src_ip not in record:
                record[src_ip] = []

            if dst_port not in record[src_ip]:
                record[src_ip].append(dst_port)

            if len(record[src_ip]) >= PORT_SCAN_THRESHOLD:
                print(f"{src_ip} 尝试端口扫描（IP可伪造仅供参考）")
                del record[src_ip]

sniff(iface="eth0", prn=packet_callback, filter="tcp")
