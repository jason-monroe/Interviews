#!/bin/bash

cat ~/findhost/input/ip_chunk* > ~/findhost/input/target_host_final.txt
nmap=$(which nmap)
if [[ -z $nmap ]]; then
export DEBIAN_FRONTEND=noninteractive 
 sudo apt-get -y install nmap 
fi
nmap -T5 -A -p 1-65535 -iL ~/findhost/input/target_host_final.txt -oG ~/findhost/input/nmap.gnmap

python3 findhost/input/port-finder.py findhost/input/nmap.gnmap > findhost/output/found-hosts.csv

