
# Shadow utils

## Install
```bash
apt install shadow-utils
yum/dnf install shadow-utils
pacman -S shadow
```

## Start podman socket for the user

You'll probably want to do this as many applications interact with the socket.

Run as your podman user:

```bash
systemctl --user start podman.socket

# Don't forget to enable it if you want it to be available after restart
systemctl --user enable podman.socket
```


## User namespace stuff


### Expected capabilities

```bash
sudo getcap /usr/bin/newuidmap /usr/bin/newgidmap
# /usr/bin/newuidmap cap_setuid=ep
# /usr/bin/newgidmap cap_setgid=ep

```


### Permissions

``` bash

ls -la /usr/bin/newuidmap /usr/bin/newgidmap
#.rwxr-xr-x@   33k root  1 Apr 05:19 newgidmap
#.rwxr-xr-x@   33k root  1 Apr 05:19 newuidmap

# or, I've had troubles with this one on Arch but it should be correct.
#.rwsr-xr-x   33k root  1 Apr 05:19 newgidmap
#.rwsr-xr-x   33k root  1 Apr 05:19 newuidmap
```


## Verify namespace is configured

If this isn't set to y then it's a kernel level issue.
```bash
zgrep CONFIG_USER_NS /proc/config.gz
#CONFIG_USER_NS=y
#CONFIG_USER_NS_UNPRIVILEGED=y
```


## Troubleshooting

### newuidmap fails to set

Remove the shadow and Podman applications.  Reinstall.
```bash
sudo pacman -Rdd shadow
sudo pacman -R podman

rm -rf ~/.local/share/containers
sudo pacman -S shadow podman
```


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

