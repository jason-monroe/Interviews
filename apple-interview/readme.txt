#The Assignment 
3 Business Day Completion Time:
Write a scanner in either Python, Go, or Bash which will test web servers basic auth for credentials of root:root.

Things to take into account:
Scaleability - You may need to run this on tens of thousands of hosts.
Ports - The service may be running on an alternative port.
Output - Is the output of the tool easy to decipher and could you easily use the input for other tools?
Accuracy - How can you confirm the result is a true positive?

The Candidate Needs to provide the following:

* The code
* Any documentation on how to execute the code

# The way that I interpreted the problem. Imagine you have a X million nodes that need to be tested. You're going to need essentially a cluster of nodes and some kind of leader thing to make this work. I wanted to make this not dependent on kubernetes so it's a collection of python and bash scripts to make this work for however many nodes you can spare to scan. 


# Purpose 
can you create some scripty bits that would show command line and programming skills for a pipeline

#Setup 
You'll need a couple of delegate nodes to facilitate the work 
you can use 127.0.0.1 if you like 
where you would setup your own ~/.ssh/id_rsa.pub in your ~/.ssh/authorized_keys file if you only have one node
Else you would put those in the 
./findhost/input/worker-nodes.txt   
The script assumes you can ssh around and scp as the same user you are running as 
script also assumes you have net-addr to facilitate the IP list 
so you might need 
apt-get -y install python3-netaddr

#Usage 
from the parent directory you would run 
bash ./leader.sh 143.198.58.216,146.190.59.85
The IPs provided could be CIDR or single IPs 

it will create a bunch of files 50k max ips in 
findhost/input/ip_chunks_N.csv 

then based on the number of do a round robin and send the chunks to 
each of the worker nodes and place the chunk in each of the worker nodes ~/findhost/input/ directory 

From there the python script the parses the nmap output and uses request to make the calls to the subsequent targets is also pushed over 
There is a node controller that will install nmap if it's not already there in the path 

the connection is made to the worker nodes to execute the node-controller script without any input 

# After some time the leader doesn't periodically check the nodes to see if they are done because (unfinished feature ) 
You would wait a little while and then run the 
bash ./report.sh 
which will connect to the worker nodes pull back to the CSV and then product a report kinda like 

======================REPORT START =============================================


Total instances of root:root password found: 3 across total uniq hosts: 2


=====================REPORT END ================================================
