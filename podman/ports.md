## Binding to privileged ports(<1024)

### Sysctl and Port forwarding w/ firewall(Easiest)

Generally, the easiest/best solution seems to be to lower the privileged port
to the what you need, i.e. 80 and then redirect all other ports using a firewall.

```bash
sysctl net.ipv4.ip_unprivileged_port_start=80
# or persist
sysctl -w net.ipv4.ip_unprivileged_port_start=80

# (Optional, but recommended) Block all other ports with a firewall.
iptables -I INPUT -p tcp --dport 80:1024 -j DROP
iptables -I INPUT -p udp --dport 80:1024 -j DROP
```

Obviously, this isn't ideal but it does solve the problem and the port is only 
exposed when something isn't bound to it.

### Capabilities

If you're feeling brave, you can go the capability route but results are mixed
on this one.  Many people, including myself, report failing to get this to work
with Podman.

```bash
sudo setcap 'cap_net_bind_service+eip' /usr/bin/podman 
```

Also, this isn't very secure anyways since any program that uses podman can bind
to any port now.

