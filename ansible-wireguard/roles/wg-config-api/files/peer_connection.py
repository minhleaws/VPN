import os
from os import path
from threading import Thread
from netaddr import IPNetwork
import json
import sys

cidr = os.environ['CIDR']
client_dir = os.environ['CLIENT_DIR']
number_of_clients = os.environ['NUMBER_OF_CLIENTS']
server_config_file = os.environ['SERVER_CONF_FILE']

network = IPNetwork(cidr)
range_ip = list(network)[2:int(number_of_clients)+2]

def cofig_peer(client_ip, server_config_file, public_key_path):
    publickey = open(public_key_path, 'r').read().split('\n')   # array

    peer_template = """\
## start added by ansible {client_ip}
[Peer]
PublicKey = {publickey}
AllowedIPs = {client_ip}/32
## stop added by ansible {client_ip}
""".format(client_ip=client_ip, publickey=publickey[0])

    with open(server_config_file, 'a') as f:
        f.write(peer_template)


def filter_lines(f, start_delete, stop_delete):
    """
    Given a file handle, generate all lines except those between the specified
    text markers.
    """
    lines = iter(f)
    try:
        while True:
            line = next(lines)
            if start_delete in line:
                # Discard all lines up to and including the stop marker
                while stop_delete not in line:
                    line = next(lines)
                line = next(lines)
            yield line
    except StopIteration:
        return

def redact_files(server_config_file, start_delete, stop_delete):
    """
    Edit all files named "fileName.xml" under the current directory, stripping
    out text between the specified text markers.
    """

    with open(server_config_file, 'r+') as f:
        filtered = list(filter_lines(f, start_delete, stop_delete))
        f.seek(0)
        f.writelines(filtered)
        f.truncate()

if __name__ == '__main__':
    for ip in range_ip:
        start_delete = "## start added by ansible {client_ip}".format(client_ip=ip)
        stop_delete  = "## stop added by ansible {client_ip}".format(client_ip=ip)
        redact_files(server_config_file, start_delete, stop_delete)
        
        public_key_path = "{client_dir}/{ip}/publickey".format(client_dir=client_dir,ip=ip)
        cofig_peer(ip, server_config_file, public_key_path)
