module KeyBindings (
    KeyBinding
  , xmonadBasics

  , windowNavigation
  , windowSizing
  , layoutControl
  , workspaceChanging
  , multiHeadNavigation

  , defaultPromptConf
  , processControl

  , MusicCommands (..)
  , defaultMusicCommands
  , musicControl

  , ExtraCommands (..)
  , defaultExtraCommands
  , extraKeys

  , m
  ) where

import Defaults (defaultTerminal)

import XMonad ( (.|.) )
import XMonad.Core
import XMonad.Operations ( windows, sendMessage, refresh, screenWorkspace, kill, withFocused )
import XMonad.Layout ( IncMasterN(IncMasterN), Resize(Shrink, Expand), ChangeLayout(NextLayout) )
import XMonad.Layout.Gaps ( GapMessage( ToggleGaps ))
import qualified XMonad.StackSet as W
import XMonad.Layout.ResizableTile ( MirrorResize(MirrorShrink, MirrorExpand) )
import XMonad.Prompt (XPConfig(..), defaultXPKeymap, mkXPrompt, deleteAllDuplicates, XPPosition(..) )
import XMonad.Prompt.Shell (Shell(..), getCommands, getShellCompl, shellPrompt)

import System.Exit ( exitWith, ExitCode(ExitSuccess) )
import Graphics.X11.Types
import Graphics.X11.ExtraTypes
import Data.Default (def)
import Data.List (isPrefixOf, nub, filter, notElem)

import Passwords

-- alias the lead keys
m :: KeyMask
m = mod4Mask
s :: KeyMask
s = shiftMask
ms :: KeyMask
ms = m .|. s
c :: KeyMask
c = controlMask
mc :: KeyMask
mc = m .|. c

type KeyBinding = ((KeyMask, KeySym), (X ()))

xmonadBasics :: String -> String -> [KeyBinding]
xmonadBasics killcmd lockcmd =
  -- These are the base keys, for things like starting/stopping xmonad
  [ ((m       , xK_q), spawn killcmd)
  , ((ms      , xK_q), io (exitWith ExitSuccess))
  , ((ms , xK_Return), spawn defaultTerminal)
  , ((m       , xK_z), spawn lockcmd)
  ]

windowNavigation :: [KeyBinding]
windowNavigation =
  -- These are the keys to switch the focused window on the workspace
  [ ((m , xK_Tab), windows W.focusDown)
  , ((m   , xK_j), windows W.focusDown)
  , ((m   , xK_k), windows W.focusUp)
  ]

windowSizing :: [KeyBinding]
windowSizing =
  -- These are the keys to modify the sizing of the windows on the workspace
  [ ((m  , xK_h), sendMessage Shrink)
  , ((m  , xK_l), sendMessage Expand)
  , ((m  , xK_n), refresh)
  -- ResizableTall layout keys
  , ((ms , xK_h), sendMessage MirrorShrink)
  , ((ms , xK_l), sendMessage MirrorExpand)
  -- Gaps
  , ((ms , xK_space), sendMessage ToggleGaps)
  ]

layoutControl :: [KeyBinding]
layoutControl =
  -- These are the keys used to modify the count of master windows and order
  [ ((m   , xK_space),  sendMessage NextLayout)
  , ((ms      , xK_j),  windows W.swapDown)
  , ((ms      , xK_k),  windows W.swapUp)
  , ((m   , xK_comma),  sendMessage (IncMasterN 1))
  , ((m  , xK_period),  sendMessage (IncMasterN (-1)))
  , ((m       , xK_t),  withFocused $ windows . W.sink)
  ]

workspaceChanging :: XConfig Layout -> [KeyBinding]
workspaceChanging conf =
  -- mod + # goes to workspace
  [((m, k) , windows $ W.greedyView i)
    | (i, k) <- zip ws [xK_1 .. xK_9]
  ]
  ++
  -- mod + shift + # moves window to workspace
  [((ms, k), windows $ W.shift i)
    | (i, k) <- zip ws [xK_1 .. xK_9]
  ]
  where
    ws = (workspaces conf)

multiHeadNavigation :: [KeySym] -> [KeyBinding]
multiHeadNavigation monitorKeys =
  -- mod + [monitorKeys] goes to display
  [((m, k) , screenWorkspace screen >>= flip whenJust (windows . W.view))
    | (k, screen) <- zip monitorKeys [0..]
  ]
  ++
  -- mod + shift + [monitorKeys] shifts window to display
  [((ms, k) , screenWorkspace screen >>= flip whenJust (windows . W.shift))
    | (k, screen) <- zip monitorKeys [0..]
  ]

defaultPromptConf :: XPConfig
defaultPromptConf = def
  { font = "-*-ubuntumono nerd font mono-medium-r-normal-*-16-*-*-*-*-*-*-*"
  , bgColor = "#333333"
  , fgColor = "#EEEEEE"
  , fgHLight = "#333333"
  , bgHLight = "#4422EE"
  , borderColor = "#333333"
  , promptBorderWidth = 0
  , position = Top
  , height = 16
  , historySize = 16
  , promptKeymap = defaultXPKeymap
  , completionKey = (0, xK_Tab)
  , defaultText = ""
  , autoComplete = Nothing
  , showCompletionOnTab = True
  , searchPredicate = isPrefixOf
  }

processControl :: XPConfig -> [String] -> [KeyBinding]
processControl promptConf ignoredCmds =
  -- These are the keys used to add/remove processes
  [ ((ms , xK_Return), spawn $ defaultTerminal)
  , ((ms      , xK_c), kill)
  , ((m       , xK_p), spawn "rofi -show combi")
  , ((m       , xK_bracketleft), spawn "kill -s USR1 $(pidof deadd-notification-center)")
  ]
  ++
  -- This is an experiment with the search prompt
  [ ((mc       , xK_p), passwordPrompt passConf)
  ]
  where
      passConf = promptConf
        { historySize = 0
        }

data MusicCommands = MusicCommands
  { next :: String
  , prev :: String
  , toggle :: String
  }

defaultMusicCommands :: MusicCommands
defaultMusicCommands = MusicCommands
  { next = "playerctl next"
  , prev = "playerctl prev"
  , toggle = "playerctl play-pause"
  }

musicControl :: MusicCommands -> [KeyBinding]
musicControl cmds =
  -- These are the keys used to control MPD playback
  [ ((m , xK_Right), spawn (next cmds))
  , ((m ,  xK_Down), spawn (toggle cmds))
  , ((m ,  xK_Left), spawn (prev cmds))
  -- These are the XF86 keys
  , ((0 , xF86XK_AudioPlay), spawn (toggle cmds))
  , ((0 , xF86XK_AudioPrev), spawn (prev cmds))
  , ((0 , xF86XK_AudioNext), spawn (next cmds))
  ]

data ExtraCommands = ExtraCommands
  { audio_up :: String
  , audio_down :: String
  , audio_toggle :: String
  , mon_up :: String
  , mon_down :: String
  , kbd_up :: String
  , kbd_down :: String
  }

defaultExtraCommands :: ExtraCommands
defaultExtraCommands = ExtraCommands
  { audio_up = "pulsemixer --change-volume +5"
  , audio_down = "pulsemixer --change-volume -5"
  , audio_toggle = "pulsemixier --toggle-mute"

  , mon_up = ""
  , mon_down = ""

  , kbd_up = ""
  , kbd_down = ""
  }

extraKeys :: ExtraCommands -> [KeyBinding]
extraKeys cmds =
  -- These are tying actions to the 'action' keys (the volume, launcher, brightness keys)
  [ ((0 ,  xF86XK_AudioRaiseVolume) , spawn (audio_up cmds))
  , ((0 ,  xF86XK_AudioLowerVolume) , spawn (audio_down cmds))
  , ((0 ,         xF86XK_AudioMute) , spawn (audio_toggle cmds))
  , ((ms,                 xK_Right) , spawn (audio_up cmds))
  , ((ms,                  xK_Left) , spawn (audio_down cmds))
  , ((ms,                  xK_Down) , spawn (audio_toggle cmds))
  , ((0 ,   xF86XK_MonBrightnessUp) , spawn (mon_up cmds))
  , ((0 , xF86XK_MonBrightnessDown) , spawn (mon_down cmds))
  , ((0 ,   xF86XK_KbdBrightnessUp) , spawn (kbd_up cmds))
  , ((0 , xF86XK_KbdBrightnessDown) , spawn (kbd_down cmds))
  ]
