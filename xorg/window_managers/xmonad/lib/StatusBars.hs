module StatusBars (
    polybarDHConf
  ) where

import Data.List (elemIndex)
import qualified Colors

polybarDHConf :: String -> [String] -> PP
polybarDHConf fifo wslist = def
  { ppCurrent = pbBG "#CC339933" . pbChangeWS
  , ppVisible = pbBG "#CC333399" . pbChangeWS
  , ppHidden = pbFG "#FFFFFF" . pbChangeWS
  , ppHiddenNoWindows = pbFG Colors.hiddenPBWS . pbChangeWS
  , ppUrgent = pbOL "#FF9933" . pbChangeWS
  , ppSep = ""
  , ppWsSep = ""
  , ppOrder = \(ws:l:t:_) -> [ws]
  , ppOutput = \x -> appendFile fifo (x ++ "\n")
  }
  where
    pbBG color str = "%{B" ++ color ++ "}" ++ str ++ "%{B-}"
    pbFG color str = "%{F" ++ color ++ "}" ++ str ++ "%{F-}"
    pbUL color str = "%{u" ++ color ++ "}" ++ str ++ "%{-u}"
    pbOL color str = "%{o" ++ color ++ "}" ++ str ++ "%{-o}"
    pbChangeWS str = pbClickWS (wsIndexLookup str) str
    pbClickWS Nothing str = ""
    pbClickWS (Just i) str = "%{A1:/usr/bin/xdotool key super+" ++ (show (i + 1)) ++ ":} " ++ (wsName str) ++ " %{A}"
    wsName "NSP" = ""
    wsName ws = ws
    wsIndexLookup ws = elemIndex ws wslist
