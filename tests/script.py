import time

from scapy.all import *
import requests
import json
import random

from scapy.layers.inet import TCP, UDP, ICMP,IP

api_url = "https://network-intrusion-detection-abf8bxfsf6gaaycu.canadacentral-01.azurewebsites.net/predict"

headers = {
    'Content-Type': 'application/json'
}


def generate_packet_data():

    protocol_choice = random.choice(["tcp", "udp", "icmp"])

    if protocol_choice == "tcp":
        pkt = IP(dst="8.8.8.8") / TCP(dport=random.randint(1, 65535), flags=random.choice(["S", "A", "F", "P"])) / Raw(
            load="RandomPayload")
    elif protocol_choice == "udp":
        pkt = IP(dst="8.8.8.8") / UDP(dport=random.randint(1, 65535)) / Raw(load="RandomPayload")
    else:
        pkt = IP(dst="8.8.8.8") / ICMP()

    protocol_type = protocol_choice
    src_bytes = len(pkt[IP].payload)
    dst_bytes = random.randint(0, 1500)
    flag = pkt[TCP].flags if protocol_type == "tcp" else "N/A"

    data = {
        "duration": random.randint(0, 10),
        "protocol_type": protocol_type,
        "service": random.choice(['ftp_data', 'other', 'private', 'http', 'remote_job', 'name',
       'netbios_ns', 'eco_i', 'mtp', 'telnet', 'finger', 'domain_u',
       'supdup', 'uucp_path', 'Z39_50', 'smtp', 'csnet_ns', 'uucp',
       'netbios_dgm', 'urp_i', 'auth', 'domain', 'ftp', 'bgp', 'ldap',
       'ecr_i', 'gopher', 'vmnet', 'systat', 'http_443', 'efs', 'whois',
       'imap4', 'iso_tsap', 'echo', 'klogin', 'link', 'sunrpc', 'login',
       'kshell', 'sql_net', 'time', 'hostnames', 'exec', 'ntp_u',
       'discard', 'nntp', 'courier', 'ctf', 'ssh', 'daytime', 'shell',
       'netstat', 'pop_3', 'nnsp', 'IRC', 'pop_2', 'printer', 'tim_i',
       'pm_dump', 'red_i', 'netbios_ssn', 'rje', 'X11', 'urh_i',
       'http_8001']),
        "flag": random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH', 'RSTO', 'S1', 'RSTOS0', 'S3','S2','OTH']),
        "src_bytes": src_bytes,
        "dst_bytes": dst_bytes,
        "land": random.randint(0, 1),
        "wrong_fragment": random.randint(0, 3),
        "urgent": random.randint(0, 5),
        "hot": random.randint(0, 15),
        "num_failed_logins": random.randint(0, 5),
        "logged_in": random.randint(0, 1),
        "num_compromised": random.randint(0, 10),
        "root_shell": random.randint(0, 1),
        "su_attempted": random.randint(0, 1),
        "num_root": random.randint(0, 10),
        "num_file_creations": random.randint(0, 10),
        "num_shells": random.randint(0, 1),
        "num_access_files": random.randint(0, 5),
        "num_outbound_cmds": random.randint(0, 10),
        "is_host_login": random.randint(0, 1),
        "is_guest_login": random.randint(0, 1),
        "count": random.randint(0, 100),
        "srv_count": random.randint(0, 100),
        "serror_rate": round(random.uniform(0, 1), 2),
        "srv_serror_rate": round(random.uniform(0, 1), 2),
        "rerror_rate": round(random.uniform(0, 1), 2),
        "srv_rerror_rate": round(random.uniform(0, 1), 2),
        "same_srv_rate": round(random.uniform(0, 1), 2),
        "diff_srv_rate": round(random.uniform(0, 1), 2),
        "srv_diff_host_rate": round(random.uniform(0, 1), 2),
        "dst_host_count": random.randint(0, 255),
        "dst_host_srv_count": random.randint(0, 255),
        "dst_host_same_srv_rate": round(random.uniform(0, 1), 2),
        "dst_host_diff_srv_rate": round(random.uniform(0, 1), 2),
        "dst_host_same_src_port_rate": round(random.uniform(0, 1), 2),
        "dst_host_srv_diff_host_rate": round(random.uniform(0, 1), 2),
        "dst_host_serror_rate": round(random.uniform(0, 1), 2),
        "dst_host_srv_serror_rate": round(random.uniform(0, 1), 2),
        "dst_host_rerror_rate": round(random.uniform(0, 1), 2),
        "dst_host_srv_rerror_rate": round(random.uniform(0, 1), 2)
    }

    return data


try:
    for i in range(30):
        payload_data = {"data": generate_packet_data()}
        print(payload_data)
        response = requests.post(api_url, headers=headers, json=payload_data['data'])
        response.raise_for_status()

        response_json = response.json()
        print(f"Request {i + 1}:")
        print(json.dumps(response_json, indent=4))
        time.sleep(1)

except requests.exceptions.RequestException as e:
    print("Error:", e)
