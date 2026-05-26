import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Hyprland
import qs

Row {
    property int monitor: 0
    readonly property var icons: {
        "DEFAULT": "",
        "term": "",
        "web": "爵",
        "code": "",
        "games": "",
        "chat": "ﭮ",
        "music": "ﱘ",
        "scratch": "ﴬ",
        "video": "",
        "notes": "ﴬ"
    }
    readonly property var occupied: {
        const occ = {
        };
        for (const ws of Hyprland.workspaces.values) occ[ws.id] = ws.lastIpcObject.windows > 0
        return occ;
    }

    function iconLookup(name: string) : string {
        return icons[name] || icons["DEFAULT"];
    }

    x: 7
    y: 3
    bottomPadding: 2
    leftPadding: 2
    topPadding: 2
    rightPadding: 2
    spacing: 4

    Repeater {
        model: Hyprland.workspaces

        Rectangle {
            id: root

            required property HyprlandWorkspace modelData
            property bool hover: false
            property bool isActive: modelData.active
            property bool isFocused: modelData.focused
            property bool isOccupied: modelData.toplevels.values.length > 0
            property bool isUrgent: modelData.urgent

            visible: (modelData !== null && modelData.id >= 0 && modelData.monitor !== null && modelData.monitor.name === screen.name)
            color: {
                if (isUrgent)
                    return U.rgba(221, 136, 33, 1);

                if (isFocused)
                    return U.rgba(34, 204, 221, 1);

                if (isActive)
                    return hover ? U.rgba(34, 204, 221, 1) : U.rgba(200, 200, 200, 1);

                if (isOccupied)
                    return hover ? U.rgba(150, 150, 150, 1) : U.rgba(100, 100, 100, 1);

                return hover ? U.rgba(150, 150, 150, 1) : U.rgba(122, 122, 122, 0.3);
            }
            implicitHeight: Config.em(1.3)
            implicitWidth: Config.em(1.35)
            radius: 25

            Text {
                anchors.fill: parent
                x: 2
                y: 2
                text: iconLookup(root.modelData.name)
                color: {
                    if (isFocused || isUrgent || isActive)
                        return U.rgba(0, 0, 0, 1);

                    if (isOccupied)
                        return U.rgba(255, 255, 255, 1);

                    return "#999999";
                }
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter

                font {
                    family: "Hack Nerd Font Mono"
                    pixelSize: Config.em(1.1)
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: isFocused ? Qt.ArrowCursor : Qt.PointingHandCursor
                    onClicked: {
                        if (isFocused)
                            return ;

                        root.modelData.activate();
                    }
                    onEntered: {
                        root.hover = true;
                    }
                    onExited: {
                        root.hover = false;
                    }
                }

            }

            Behavior on color {
                enabled: Config.animations
                ColorAnimation {
                    target: root
                    duration: 200
                }

            }

        }

    }

}
