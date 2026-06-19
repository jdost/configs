//@ pragma UseQApplication
//@ pragma IconTheme Papirus-Dark
//@ pragma Env QS_NO_RELOAD_POPUP=1
//@ pragma Env QT_QUICK_CONTROLS_STYLE=Material
//@ pragma Env QT_QUICK_CONTROLS_MATERIAL_THEME=Dark

import "Bar"
import "Common"
import "Notifications"
import "OSD"
import QtQuick
import Quickshell
import "Services"
import "Sidebar"

ShellRoot {
    id: root

    Bar {
    }

    NotificationList {
        id: notificationPopups
    }

    OSD {
    }

    SidebarPanel {
        id: sidebar
    }

}
