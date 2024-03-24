import sys
import os
import re
import requests
from prettytable import PrettyTable

def get_ip_info(ip):
    url = f'http://ip-api.com/json/{ip}?fields=27137'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        as_info = data.get('as', '-')
        as_info = as_info.split(' ')[0]
        country = data.get('country', '-')
        isp = data.get('isp', '-')
        return [data['query'], as_info, country, isp]
    else:
        return [ip, '-', '-', '-']

def tracert(ip):
    result = os.popen(f"tracert {ip}").read()

    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips_found = re.findall(ip_pattern, result)
    return ips_found[1:]

def main():
    if len(sys.argv) != 2:
        print("Usage: python tracert.py [ip address or dns name]")
        sys.exit(1)

    target = sys.argv[1]
    hop_ips = tracert(target)

    print(f"Traceroute to {target}:\n")

    table = PrettyTable(["№ по порядку", "ip", "as", "country", "provider"])
    for i, ip in enumerate(hop_ips, start=1):
        ip_info = get_ip_info(ip)
        table.add_row([str(i), ip_info[0], ip_info[1], ip_info[2], ip_info[3]])

    print(table)

if __name__ == "__main__":
    main()







