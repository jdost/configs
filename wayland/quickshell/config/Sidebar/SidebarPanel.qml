import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import qs

Scope {
    id: root

    property bool shown: false;
    readonly property int width: Config.em(18);

    function toggle(screen) {
        if (shown) {
            loader.x = width
        } else {
            loader.active = true
            loader.screen = screen
            loader.x = 0
        }
        shown = !shown;
    }

    LazyLoader {
        id: loader

        property int x: width
        property var screen

        PanelWindow {
            id: sidebar

            anchors {
                top: true
                right: true
                bottom: true
            }

            color: "transparent"
            exclusionMode: ExclusionMode.Ignore
            implicitWidth: root.width
            margins.bottom: Config.em(0.3)
            margins.top: Config.em(2.3)
            screen: screen
            WlrLayershell.namespace: "quickshell::sidebar"

            Rectangle {
                id: background

                bottomLeftRadius: Config.em(0.75)
                color: U.rgba(44, 44, 44, 0.6)
                implicitWidth: root.width
                implicitHeight: sidebar.height
                topLeftRadius: Config.em(0.75)
                x: loader.x

                onXChanged: function () {
                    if (x === root.width && !root.shown) {
                        loader.active = false;
                    }
                }

                Behavior on x {
                    enabled: Config.animations
                    SmoothedAnimation {
                        velocity: 400;
                    }
                }
            }
        }
    }
}
