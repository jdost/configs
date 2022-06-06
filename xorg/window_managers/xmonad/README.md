# Legacy xmonad configs

These are unmaintained, I switched to using bspwm a while ago but wanted
to get the xmonad code added just for the legacy purpose (and if I every
decide I want to switch back).  This has a lot of history (and cruft) in
the code but is what I used for a good part of a decade...

## Layout

Most of the definitions are modular and live under the `lib/` directory,
they are not well split and could really use some love and organization.
One file that is expected (and missing) is a `Settings.hs` file that
declares the system's settings.  I have included an example in here but it
is not meant to be canonical.  I believe most of the logic should be
portable to the existing tooling, but it is all untested.

## Additional Stuff

- `polybar` - There is no straightforward polybar module for xmonad
  workspace listing, so I have a custom hook that generates polybar style
  markup and a polybar module that just tails this fifo
- `rebuild.sh` - A helper executable that manually rebuilds the xmonad
  binary, this is an issue after an upgrade where the old binary has out
  of date references and crashes, requiring a fresh rebuild.  This should
  be moved into the xinitrc hook, but I won't do that until I start
  maintaining this
