

# How to run Bnet

Download the Wine bottles flatpak, make a new 'gaming' bottle.

In the bottle, use the Bottle installer for Battle.net.


Worked for me on Wayland:
- runner: soda-9.0.1
- DXVK: dxvk-2.3.1
- VKD3D: vkd3d-proton-2.12
- Env variables(Most Important):
  - WINE_SIMULATE_WRITECOPY=1

NOTE:
Initially, BNET is frozen on startup.  To fix this, I swapped over to my syswine(sys-wine-9.0)
which at least was able to startup the login not frozen, but it was loading forever.
So, after doing that once, I swap back to the default(soda-9.0.1) and restart the app.
From there it works like normal, most likely the other run created some files or 
something.
