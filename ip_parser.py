import re
import sys

import utils


def process_ips(file_path, verbose=True):
    ip_port_map = {}
    ip_regex = r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3})(?::(?P<port>\d{1,5}))?'

    ip_count = 0

    if verbose:
        print("Reading " + file_path)

    with open(file_path, 'r') as file:
        for line in file:
            matches = re.finditer(ip_regex, line)
            for match in matches:
                ip = match.group('ip')
                port = match.group('port')

                ip_count += 1

                if ip in ip_port_map:
                    if port:
                        ip_port_map[ip].add(port)
                else:
                    ip_port_map[ip] = {port} if port else set()

    unique_ips = []
    for ip, ports in ip_port_map.items():
        if ports:  # Only add ports if they exist
            for port in ports:
                if port:
                    unique_ips.append(f"{ip}:{port}")
                else:
                    unique_ips.append(ip)
        else:
            unique_ips.append(ip)
    del ip_port_map

    if verbose:
        print("Removed " + str(ip_count - len(unique_ips)) + " Duplicate IPs")

    # removed_count = 0
    # valid_ips = []
    #
    # for ip in unique_ips:
    #     if utils.is_valid_ip(ip):
    #         valid_ips.append(ip)
    #     else:
    #         removed_count += 1
    #         print(ip)
    #
    #
    # del unique_ips
    # print("Removed " + str(removed_count) + " invalid IPs")

    if verbose:
        print("Retrieved " + str(len(unique_ips)) + " IPs")

    return unique_ips