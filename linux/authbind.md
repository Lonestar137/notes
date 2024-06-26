# Authbind

Authbind is a tool to allow non-root applications to bind to low ports(<1024)
without root permission.

Example usage

```bash
sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown jonesgc /etc/authbind/byport/80

authbind --deep python3.12 -m http.server 80
```

## Limitations

### Podman

Does NOT work with Podman since Podman runs its networking using the randomly 
mapped user namespace range configured in /etc/subuid for that user.  

Authbind doesn't know how to handle capabilities or namespaces.
