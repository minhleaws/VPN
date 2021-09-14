import os
from os import path
from threading import Thread
from netaddr import IPNetwork
import json

cidr = os.environ['CIDR']
number_of_clients = os.environ['NUMBER_OF_CLIENTS']
client_dir = os.environ['CLIENT_DIR']
json_path = os.environ['JSON_FILE_PATH']

network = IPNetwork(cidr)
range_ip = list(network)[2:int(number_of_clients)+2]

if __name__ == '__main__':
    wgConfigData = []
    for ip in range_ip:
        client_json_path = "{client_dir}/{ip}/wg.json".format(client_dir=client_dir,ip=ip)
        with open(client_json_path) as json_file:
            data = json.load(json_file)
            wgConfigData.append(data)
    template = { "wgConfigData": wgConfigData}

    with open(json_path, 'w') as json_file:
        json_file.write(json.dumps(template))
