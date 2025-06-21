from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
import pandas as pd
import os

DATA_PATH = "data/processed_packets.csv"
packet_list = []

def process_packet(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        proto = packet.proto if hasattr(packet, "proto") else None
        info = {
            "timestamp": datetime.now().isoformat(),
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "packet_len": len(packet),
            "protocol": proto
        }
        if packet.haslayer(TCP):
            info.update({
                "src_port": packet[TCP].sport,
                "dst_port": packet[TCP].dport,
                "flags": str(packet[TCP].flags)
            })
        elif packet.haslayer(UDP):
            info.update({
                "src_port": packet[UDP].sport,
                "dst_port": packet[UDP].dport
            })
        else:
            info.update({"src_port": None, "dst_port": None, "flags": None})

        packet_list.append(info)
        print(info)

# Capture 100 packets and save
sniff(prn=process_packet, store=0, count=100)

df = pd.DataFrame(packet_list)
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
df.to_csv(DATA_PATH, index=False)
