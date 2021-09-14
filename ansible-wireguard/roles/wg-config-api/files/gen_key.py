import os
from os import path
from threading import Thread
from netaddr import IPNetwork

cidr = os.environ['CIDR']
client_dir = os.environ['CLIENT_DIR']
number_of_clients = os.environ['NUMBER_OF_CLIENTS']

network = IPNetwork(cidr)
range_ip = list(network)[2:int(number_of_clients)+2]


def gen_key(private_key_path, public_key_path):
    if not (path.exists(public_key_path) or path.exists(private_key_path)):
        os.system("umask 077; wg genkey | tee %s | wg pubkey > %s" % (private_key_path, public_key_path))

def gen_key_without_thread():
    for ip in range_ip:
        private_key_path = "{client_dir}/{ip}/privatekey".format(client_dir=client_dir,ip=ip)
        public_key_path  = "{client_dir}/{ip}/publickey".format(client_dir=client_dir,ip=ip)
        gen_key(private_key_path, public_key_path)

def gen_key_thread():
    threads = []
    for ip in range_ip:
        private_key_path = "{client_dir}/{ip}/privatekey".format(client_dir=client_dir,ip=ip)
        public_key_path  = "{client_dir}/{ip}/publickey".format(client_dir=client_dir,ip=ip)

        thr = Thread(target=gen_key, args=(private_key_path, public_key_path,))
        thr.start()
        threads.append(thr)

    # wait for all threads to completed
    for thr in threads:
        thr.join()    

if __name__ == '__main__':
    gen_key_thread()
