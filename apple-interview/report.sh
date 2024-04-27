#!/bin/bash
#
ips=( $( cat ./findhost/input/worker-nodes.txt | cut -f 1 -d,  ))
for ip in "${!ips[@]}"; do
  # reporting
  scp ${ips[ip]}:~/findhost/output/found-hosts.csv ./findhost/output/${ips[ip]}-found-hosts.csv
done


total=$(grep Success findhost/output/*-found-hosts.csv  | wc -l)
uniq_hosts=$(grep Success findhost/output/*-found-hosts.csv  | cut -f 2 -d, | uniq | wc -l)
echo "======================REPORT START ============================================="
echo ""
echo ""

echo "Total instances of root:root password found: $total across total uniq hosts: $uniq_hosts"

echo ""
echo""
echo "=====================REPORT END ================================================"
