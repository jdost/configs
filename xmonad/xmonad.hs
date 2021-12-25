import XMonad
import XMonad.Core
import XMonad.Hooks.DynamicLog (dynamicLogWithPP)
import XMonad.Hooks.ManageDocks (manageDocks, docks)
import XMonad.Hooks.UrgencyHook (withUrgencyHook, NoUrgencyHook(NoUrgencyHook) )
import XMonad.Layout.IndependentScreens (countScreens)
import XMonad.Util.Run (spawnPipe, safeSpawn)

import XMonad.Hooks.FadeInactive (fadeInactiveLogHook)
import XMonad.Hooks.EwmhDesktops (ewmh)
import XMonad.Actions.UpdatePointer (updatePointer)

import qualified Data.Map as M
import Data.List (transpose)
import Graphics.X11.Types (Window)
import Graphics.X11.ExtraTypes
import System.Posix.Unistd (getSystemID, nodeName)

import Control.Monad (when)

import Colors as C
import Layouts (layoutAliases)
import Defaults
import KeyBindings
import StatusBars

import Settings

logFIFOPath :: String
logFIFOPath = "/tmp/xmonad-polybar"

main = do
  do safeSpawn "mkfifo" [logFIFOPath]

  -- make xmonad
  xmonad $ withUrgencyHook NoUrgencyHook $ ewmh $ docks def
    { terminal = defaultTerminal
    , focusFollowsMouse = defaultMouseFocus

    , borderWidth = defaultBorderWidth
    , normalBorderColor = C.unfocusedBorder
    , focusedBorderColor = C.focusedBorder

    , modMask = m
    , workspaces = workspaces'
    , keys = keys'
    , layoutHook = layouts ""
    , manageHook = manageHook def <+> hooks <+> manageDocks

    , logHook = do
        dynamicLogWithPP $ polybarDHConf logFIFOPath workspaces'
    }
-- vim: ft=haskell
