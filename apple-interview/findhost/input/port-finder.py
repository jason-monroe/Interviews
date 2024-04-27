import sys
import re
import requests
from requests.auth import HTTPBasicAuth
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to attempt connection using Basic Auth with a fallback to TLS
def attempt_connection(host, port):
    # Initial URL using HTTP
    url = f"http://{host}:{port}"
    # Try connecting using HTTP
    try:
        response = requests.get(url, auth=HTTPBasicAuth('root', 'root'))
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        print(f"Success,{host},HTTP,{port},{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP failed, attempting TLS. Error: {e}")
        # If HTTP fails, try using HTTPS
        try:
            url = f"https://{host}:{port}"
            response = requests.get(url, auth=HTTPBasicAuth('root', 'root'), verify=False)  # Ensure verify is True for TLS
            response.raise_for_status()
            #print(f"Success with TLS: {response.status_code}")
            print(f"Success,{host},TLS,{port},{response.status_code}")
        except requests.exceptions.RequestException as e:
            # Log error if both HTTP and TLS attempts fail
            logging.error(f"Both HTTP and TLS attempts failed. Error: {e}")


def parse_nmap_output(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    # Pattern to match IP addresses and HTTP port details
    ip_pattern = r"Host: (\d+\.\d+\.\d+\.\d+) \(\)"
    http_port_pattern = r"(\d+)/open/tcp//https?//"
    ip_pattern2 = r"(\d+\.\d+\.\d+\.\d+)"

    # Find all IPs
    ips = re.findall(ip_pattern, content)

    # Dictionary to hold IP and their corresponding HTTP ports
    ip_http_ports = {ip: [] for ip in ips}

    # Split content by hosts to ensure correct association of ports to IPs
    hosts = content.split('Host: ')[1:]  # Skip the first split as it's before the first host
    for host in hosts:
        # Extract IP
        ip_match = re.search(ip_pattern2, host)
        if ip_match:
            ip = ip_match.group(1)
            # Find all HTTP ports for this host
            http_ports = re.findall(http_port_pattern, host)
            ip_http_ports[ip].extend(http_ports)

    return ip_http_ports


# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to attempt connection using Basic Auth with a fallback to TLS
def attempt_connection(host, port):
    # Initial URL using HTTP
    url = f"http://{host}:{port}"
    # Try connecting using HTTP
    try:
        response = requests.get(url, auth=HTTPBasicAuth('root', 'root'))
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        print(f"Success,{host},HTTP,{port},{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP failed, attempting TLS. Error: {e}")
        # If HTTP fails, try using HTTPS
        try:
            url = f"https://{host}:{port}"
            response = requests.get(url, auth=HTTPBasicAuth('root', 'root'), verify=False)  # Ensure verify is True for TLS
            response.raise_for_status()
            #print(f"Success with TLS: {response.status_code}")
            print(f"Success,{host},TLS,{port},{response.status_code}")
        except requests.exceptions.RequestException as e:
            # Log error if both HTTP and TLS attempts fail
            logging.error(f"Both HTTP and TLS attempts failed. Error: {e}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <nmap_output_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    ip_http_ports = parse_nmap_output(filename)
    
    for ip, ports in ip_http_ports.items():
        if ports:  # Only print IPs that have HTTP ports
            for port in ports:
                attempt_connection(ip,port)
            #print(f"IP: {ip}, HTTP Ports: {', '.join(ports)}")
            


