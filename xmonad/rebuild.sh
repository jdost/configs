#!/usr/bin/env bash

set -euo pipefail

cd $HOME/.xmonad
exec ghc --make xmonad.hs \
    -i \
    -ilib \
    -dynamic \
    -fforce-recomp \
    -main-is main \
    -v0 \
    -o xmonad-x86_64-linux
