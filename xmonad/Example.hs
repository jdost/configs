module Settings where

import Layouts
import Hooks
import Defaults
import KeyBindings
import StatusBars

import XMonad
import qualified XMonad.StackSet as W
import XMonad.Hooks.ManageDocks (avoidStruts)
import XMonad.Layout.LayoutHints (layoutHints)
import XMonad.Layout.PerWorkspace (onWorkspace)
import XMonad.Layout.NoBorders (smartBorders)

import qualified Data.Map as M
import Graphics.X11.ExtraTypes

workspaces' :: [String]
workspaces' = ["code", "web", "chat"]

keys' :: XConfig Layout -> M.Map (KeyMask, KeySym) (X ())
keys' c = M.fromList $ []
  ++ KeyBindings.xmonadBasics defaultKillCmd defaultLockCmd
  ++ KeyBindings.windowNavigation
  ++ KeyBindings.multiHeadNavigation [xK_o, xK_i]
  ++ KeyBindings.windowSizing
  ++ KeyBindings.layoutControl
  ++ KeyBindings.processControl defaultPromptConf []
  ++ KeyBindings.musicControl defaultMusicCommands
  ++ KeyBindings.extraKeys defaultExtraCommands
  ++ KeyBindings.workspaceChanging c

hooks :: ManageHook
hooks = (composeAll . concat $
  [ setShifts "web" browsers
  , setShifts "chat" chats
  , setIgnores ignores
  , makeFloat floats
  ])

layouts _ = smartBorders $ avoidStruts
    $ onWorkspace "code" (normal ||| full)
    $ onWorkspace "web" (browser ||| full)
    $ onWorkspace "chat" (full)
    $ (normal ||| Mirror normal ||| full)
  where
    nconf   = defaultNormalConf
    normal  = normalLayout nconf
    bconf   = defaultBrowserConf
    browser = browserLayout bconf
    fconf   = defaultFullConf
    full    = fullLayout fconf
