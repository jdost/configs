module Colors where

focusedBorder :: String
focusedBorder = "#33CC33"

unfocusedBorder :: String
unfocusedBorder = "#333333"

dzenFG :: String
dzenFG = "#EEEEEE"
dzenBG :: String
dzenBG = "#333333"

type DzenColor = (String, String)

focusedWS    :: DzenColor
focusedWS    = ("#333333", "#339933") -- Active WS
focusedPBWS = "#339933"
unfocusedWS  :: DzenColor
unfocusedWS  = ("#333333", "#3399FF") -- WS on secondary monitor
unfocusedPBWS = "#3399FF"
urgentWS     :: DzenColor
urgentWS     = ("#333333", "#FF9933") -- WS has triggered an UrgencyHook
urgentPBWS = "#FF9933"
hiddenWS     :: DzenColor
hiddenWS     = (   dzenFG, "#444444") -- WS w/ windows, but not visible
hiddenPBWS = "#444444"
emptyWS      :: DzenColor
emptyWS      = ("#999999",    dzenBG) -- WS w/o windows, not visible
activeTitle  :: DzenColor
activeTitle  = ("#66CC66",    dzenBG) -- Title of focused window
activeLayout :: DzenColor
activeLayout = (   dzenFG, "#3939EE") -- Name of focused WS' layout
