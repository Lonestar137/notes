
## Start podman socket for the user

You'll probably want to do this as many applications interact with the socket.

Run as your podman user:

```bash
systemctl --user start podman.socket

# Don't forget to enable it if you want it to be available after restart
systemctl --user enable podman.socket
```

Socket will be available at `$XDG_RUNTIME_DIR/podman/podman.sock`

