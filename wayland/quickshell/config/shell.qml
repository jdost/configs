//@ pragma UseQApplication
//@ pragma Env QS_NO_RELOAD_POPUP=1
//@ pragma Env QS_ICON_THEME=Papirus-Dark
//@ pragma Env QT_QUICK_CONTROLS_STYLE=Material
//@ pragma Env QT_QUICK_CONTROLS_MATERIAL_THEME=Dark

import QtQuick
import Quickshell
import "Bar"
import "Common"
import "Notifications"
import "OSD"
import "Services"

ShellRoot {
    id: root

    Bar {
    }

    NotificationList {
    }

    OSD {
    }
}
