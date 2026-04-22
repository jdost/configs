import QtQuick
import QtQuick.Layouts
import Quickshell
import qs

Rectangle {
    id: left

    Layout.alignment: Qt.AlignLeft
    Layout.bottomMargin: 8
    Layout.leftMargin: 8
    Layout.topMargin: 4
    implicitHeight: childrenRect.height + 6
    implicitWidth: childrenRect.width + 12
    color: U.rgba(0, 0, 0, 0.4)
    radius: Config.em(1.2)

    HyprlandWidget {
    }

}
