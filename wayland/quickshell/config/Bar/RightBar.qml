import "./Icons"
import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import qs

Rectangle {
    id: right

    property int monitor: 0

    Layout.alignment: Qt.AlignRight
    Layout.bottomMargin: 8
    Layout.rightMargin: 8
    Layout.topMargin: 4
    color: Qt.rgba(0, 0, 0, 0.4)
    radius: Config.em(1.2)
    implicitHeight: childrenRect.height + 2
    implicitWidth: childrenRect.width + 16

    Row {
        readonly property real topPadding: 5

        y: 1
        x: 8
        height: childrenRect.height + 10
        width: childrenRect.width
        spacing: Config.em(0.2)

        Spacer { width: Config.em(0.1) }

        TrayWidget {
        }

        IconWidget {
        }

        ClockWidget {
        }

    }

}
