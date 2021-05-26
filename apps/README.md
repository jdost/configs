# apps

I often have some occasionally used applications that I don't want to
become part of my regular updates and have general access to my system so
Itry and run them inside containers.  These are various applications
I have set up in that pattern.  They often have a Dockerfile, desktop
entry, and run script (that is pretty copy pasted) for building and
launching the image.  Most will volume mount a folder from the
corresponding location in the user's homedir (like under
`~/.config/<app_name>`) to carry configuration and state between runs.
