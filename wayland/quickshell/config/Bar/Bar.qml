import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import qs

Variants {
    model: Quickshell.screens

    delegate: Component {
        PanelWindow {
            id: bar

            readonly property bool isPrimary: (Config.primaryMonitor === undefined || modelData.name === Config.primaryMonitor)
            required property var modelData

            color: "transparent"
            exclusiveZone: height
            implicitHeight: Config.em(2.2)
            screen: modelData
            WlrLayershell.namespace: "quickshell::bar"

            anchors {
                top: true
                left: true
                right: true
            }

            RowLayout {
                id: layout

                uniformCellSizes: false

                anchors {
                    left: parent.left
                    right: parent.right
                }

                LeftBar {
                }

                RightBar {
                }

            }

        }

    }

}
