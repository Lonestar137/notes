

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


Another thing, I'm trying is to add it to Steam as non-steam game.
So, just add the HOTS.exe as a non-steam game, specify the proton version and 
go.  It will prompt you to reinstall bnet but that's fine, everything else
works as expected.


## TLDR

Issues starting the launcher usually boil down to a few things:

- Wine/Proton version(Try latest or a stable version)
- System installed dependencies, it has a lot of random packages it depends on.
  Just ask an LLM for a list of packages for your distribution required for
  Battle.net.
