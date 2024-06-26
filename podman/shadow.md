
# Shadow utils

## Install
```bash
apt install shadow-utils
yum/dnf install shadow-utils
pacman -S shadow
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

