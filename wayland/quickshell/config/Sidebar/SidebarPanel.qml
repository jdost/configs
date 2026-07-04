import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import qs

Scope {
    id: root

    property bool shown: false
    property ShellScreen screen
    readonly property int width: Config.em(18)

    function toggle(screen) {
        if (shown) {
            loader.x = width;
        } else {
            loader.active = true;
            root.screen = screen;
            loader.x = 0;
        }
        shown = !shown;
    }

    LazyLoader {
        id: loader

        property int x: width

        PanelWindow {
            id: sidebar

            color: "transparent"
            exclusionMode: ExclusionMode.Ignore
            implicitWidth: root.width
            margins.bottom: Config.em(0.3)
            margins.top: Config.em(2.3)
            screen: root.screen
            WlrLayershell.namespace: "quickshell::sidebar"

            anchors {
                top: true
                right: true
                bottom: true
            }

            Rectangle {
                id: background

                bottomLeftRadius: Config.em(0.75)
                color: U.rgba(44, 44, 44, 0.6)
                implicitWidth: root.width
                implicitHeight: sidebar.height
                topLeftRadius: Config.em(0.75)
                x: loader.x
                onXChanged: function () {
                    if (x === root.width && !root.shown)
                        loader.active = false;
                }

                Behavior on x {
                    enabled: Config.animations

                    SmoothedAnimation {
                        velocity: 400
                    }
                }

                ColumnLayout {
                    y: Config.em(1)
                    width: root.width

                    Calendar {
                        Layout.preferredWidth: root.width
                    }

                    ToggleWidget {
                        Layout.preferredWidth: root.width
                    }

                    NotificationHistory {
                        Layout.fillHeight: true
                        Layout.preferredWidth: root.width
                    }
                }
            }
        }
    }
}
