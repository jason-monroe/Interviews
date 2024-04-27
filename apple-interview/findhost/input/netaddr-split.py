#!/usr/bin/python3
import sys
from netaddr import IPNetwork
import csv

def generate_ips(cidr):
    return (str(ip) for ip in IPNetwork(cidr))

def write_ips_to_csv(ips, base_filename):
    chunk_size = 50000
    for i, chunk in enumerate(chunked(ips, chunk_size)):
        filename = f"{base_filename}_{i+1}.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for ip in chunk:
                writer.writerow([ip])
        print(f"Written {filename}")

def chunked(iterable, chunk_size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <CIDR> <COMMA> <CIDR>")
        sys.exit(1)
    
    cidr_input = sys.argv[1]
    try:
        # Assuming the CIDR input can be multiple, separated by commas
        cidrs = cidr_input.split(',')
        ips = (ip for cidr in cidrs for ip in generate_ips(cidr))
        base_filename = "./findhost/input/ip_chunks"
        write_ips_to_csv(ips, base_filename)
    except Exception as e:
        print(f"An error occurred: {e}")

