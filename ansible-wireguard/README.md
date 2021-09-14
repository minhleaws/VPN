## Notes    
- Supported on Ubuntu 18.04
- Ansible version 2.9.0
- Default wireguard subnet: 172.16.128.0/24
- Default wireguard interface on both server & client: wg0
- Default wireguard server listent address 172.16.128.1/24 & port 51820 (udp)
- Default wireguard client listent port is 51821 (udp)

## Install Wireguard on Server VM
```sh
ansible-playbook -i inventories/hosts vpn_server.yml
```

## Install Wireguard Clients
```sh
ansible-playbook -i inventories/hosts vpn_client.yml --extra-vars "target=wireguard_client_1"
```

## Install Wireguard client & peer connection on both client & server
### Setup Peer connection on server & client
```sh
export SERVER_PUBKEY='9dBGVJK71VYT/tpJSkquJI8ZtQfGqDVGZL3iDSi2mUY='
export CLIENT_PUBKEY='NMxb7X3i8EFY5uugaiOoFXpYc8EmtstDClOdqr0NqF8='

ansible-playbook -i inventories/hosts peer_connection.yml \
--extra-vars "wireguard_client_publickey=${CLIENT_PUBKEY}" \
--extra-vars "wireguard_server_publickey=${SERVER_PUBKEY}" \
--extra-vars "target=wireguard_client_1"
```

## Generate Client VPN
Client_ip - random client for sub-network 172.16.128.0-254
```sh
export CLIENT_IP='172.16.128.15'
ansible-playbook -i inventories/hosts generate_client.yml --extra-vars "client_ip=$CLIENT_IP"

# Get client vpn file
scp 80.243.180.201:/etc/wireguard/clients/wg-$CLIENT_IP.conf ./
```

## Generate & Upload wgConfig (client)

```sh
ansible-playbook -i inventories/hosts wg-config-api.yml \
-e "number_of_clients=10000" \
-e "serverId=16"
```
