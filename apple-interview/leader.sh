#!/bin/bash
# counter file
# Check if there are no arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 IP,IP,IP or CIDR,CIDR,CIDR [arg2 ...]"
    exit 1
fi

python3 ./findhost/input/netaddr-split.py "$@"

# Define the list of files
files=( $( ls ./findhost/input/ip_chunk*   ))

# Define the list of IP addresses
ips=( $( cat ./findhost/input/worker-nodes.txt | cut -f 1 -d,  ))

# Get the number of IPs to cycle through them if necessary
num_ips=${#ips[@]}

# Loop through each file
for i in "${!files[@]}"; do
  # Calculate the index for the current IP, cycling through IPs if there are more files than IPs
  ip_index=$((i % num_ips))
  
  # Print the current file and its corresponding IP
  echo "${files[i]} - ${ips[ip_index]}"
  ssh ${ips[ip_index]} "mkdir -p ~/findhost/{input,output}"
  scp ${files[i]} ${ips[ip_index]}:~/findhost/input/ 
  scp ./findhost/input/port-finder.py ${ips[ip_index]}:~/findhost/input/
  scp ./findhost/input/node-controller.sh ${ips[ip_index]}:~/findhost/input/
  ssh -n -f ${ips[ip_index]} "nohup bash ~/findhost/input/node-controller.sh > /dev/null 2>&1 &"
done

