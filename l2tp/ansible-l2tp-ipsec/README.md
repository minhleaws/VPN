# L2TP/IPSec with Ansible

## 1. Installation
**Note**: Please re-check the variables in `group_vars/tag_vpn_servers.yml` file before you run this playbook

```
ansible-playbook install_configure_l2tp_ipsec.yml
```

## 2. Add / Remove vpn user
2.1 Update list user in `group_vars/tag_vpn_servers.yml` file

```yml
vpn_credentials:
  - vpn_user_name: user1
    vpn_password: password_user1

  - vpn_user_name: user3
    vpn_password: password_user3

  - vpn_user_name: foo
    vpn_password: bar
```

2.2 Run the playbook below to apply the change

```sh
ansible-playbook manage_vpn_user.yml
```

## 3. Configure IPsec/L2TP VPN Clients
Reference: https://github.com/hwdsl2/setup-ipsec-vpn/blob/master/docs/clients.md

3.1 Ubuntu Client (demo)

![](demo-l2tp-ubuntu-client-conf.mov)
