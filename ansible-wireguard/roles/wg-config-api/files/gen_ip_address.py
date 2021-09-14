from netaddr import IPNetwork
import os

cidr = os.environ['CIDR']
number_of_clients = os.environ['NUMBER_OF_CLIENTS']
ip_range_file = os.environ['IP_RANGE_FILE']

network = IPNetwork(cidr)
range_ip = list(network)[2:int(number_of_clients)+2]
with open(ip_range_file, 'a') as f:
    for ip in range_ip:
        print(ip)
        f.write('%s\n' % ip)
