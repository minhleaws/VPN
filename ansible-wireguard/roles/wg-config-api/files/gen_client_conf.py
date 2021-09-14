import os
from os import path
from threading import Thread
from netaddr import IPNetwork
import json

cidr = os.environ['CIDR']
client_dir = os.environ['CLIENT_DIR']
number_of_clients = os.environ['NUMBER_OF_CLIENTS']
ip_prefix = os.environ['IP_PREFIX']
client_port = os.environ['CLIENT_PORT']
external_dns = os.environ['EXTERNAL_DNS']
server_pubkey = os.environ['SERVER_PUBLIC_KEY']
allow_ip = os.environ['ALLOW_IP']
endpoint = os.environ['ENDPOINT']
server_port = os.environ['SERVER_PORT']
serverId = os.environ['SEVER_ID']

network = IPNetwork(cidr)
range_ip = list(network)[2:int(number_of_clients)+2]


def gen_client(client_ip, config_path, json_path, private_key_path, public_key_path):
    privatekey = open(private_key_path, 'r').read().split('\n') # array
    publickey = open(public_key_path, 'r').read().split('\n')   # array

    # Generate GW config file
    wg_conf_template = """\
[Interface]
Address = {client_ip}/{ip_prefix}
ListenPort = {client_port}
PrivateKey = {privatekey}
DNS = {external_dns}

[Peer]
PublicKey = {server_pubkey}
AllowedIPs = {allow_ip}
Endpoint = {endpoint}:{server_port}
""".format( client_ip=client_ip, 
            ip_prefix=ip_prefix, 
            client_port=client_port,
            privatekey=privatekey[0], 
            external_dns=external_dns,
            server_pubkey=server_pubkey, 
            allow_ip=allow_ip, 
            endpoint=endpoint, 
            server_port=server_port )

    # Generate GW json config file
    interface_addr = "{client_ip}/{ip_prefix}".format(client_ip=client_ip, ip_prefix=ip_prefix)
    init_endpoint = "{endpoint}:{server_port}".format(endpoint=endpoint, server_port=server_port)

    wg_json_template = {
        "serverId": int(serverId), 
        "wgConfig": { 
            "Interface": {
                "Address": interface_addr,
                "ListenPort": int(client_port),
                "PrivateKey": privatekey[0],
                "DNS": external_dns
            },
            "Peer": {
                "PublicKey": server_pubkey,
                "AllowedIPs": allow_ip,
                "Endpoint": init_endpoint
            }
        }
      }

    with open(config_path, 'w') as f:
            f.write(wg_conf_template)

    with open(json_path, 'w') as f:
            f.write(json.dumps(wg_json_template))

def gen_key_without_thread():

    for ip in range_ip:
        private_key_path = "{client_dir}/{ip}/privatekey".format(client_dir=client_dir,ip=ip)
        public_key_path  = "{client_dir}/{ip}/publickey".format(client_dir=client_dir,ip=ip)
        config_path      = "{client_dir}/{ip}/wg.conf".format(client_dir=client_dir,ip=ip)
        json_path        = "{client_dir}/{ip}/wg.json".format(client_dir=client_dir,ip=ip)
        gen_client(ip, config_path, json_path, private_key_path, public_key_path)

if __name__ == '__main__':
    gen_key_without_thread()
