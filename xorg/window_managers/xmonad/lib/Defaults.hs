module Defaults where

import Graphics.X11.Xlib.Types (Dimension)
import Graphics.X11.Types

defaultTerminal :: String
defaultTerminal = "alacritty"

defaultMouseFocus :: Bool
defaultMouseFocus = False

defaultBorderWidth :: Dimension
defaultBorderWidth = 4

defaultKillCmd :: String
defaultKillCmd = "xmonad --recompile; xmonad --restart"

defaultLockCmd :: String
defaultLockCmd = "xset s activate"

defaultMHKeys :: [KeySym]
defaultMHKeys = [xK_w, xK_e, xK_r]

homeBin :: String
homeBin = "~/.local/bin/"
