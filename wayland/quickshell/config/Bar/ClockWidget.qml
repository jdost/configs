import QtQuick
import QtQuick.Controls
import Quickshell
import qs
import qs.Sidebar

Rectangle {
    id: root

    property var screen

    color: "transparent"
    implicitWidth: display.width + 12
    implicitHeight: display.height + 4
    radius: 15
    y: parent.topPadding

    Text {
        id: display

        text: Qt.formatDateTime(clock.date, "hh:mm:ss")
        color: "#FFFFFF"
        font.family: "monospace"
        font.pixelSize: Config.em(0.7)
        x: 6
        y: Config.em(0.15)
    }

    MouseArea {
        id: mouse

        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            sidebar.toggle(screen)
        }
        onEntered: {
            tooltip.open();
        }
        onExited: {
            tooltip.close();
        }
    }

    ToolTip {
        id: tooltip

        delay: 500
        padding: 4
        popupType: Popup.Native
        y: 1.5 * root.height

        contentItem: Text {
            text: Qt.formatDateTime(clock.date, "ddd MM/dd/yyyy")
            color: U.rgba(17, 17, 17, 1)
            font.pixelSize: Config.em(0.7)
        }

        background: Rectangle {
            radius: 15
            color: U.rgba(212, 212, 212, 0.65)
        }

        enter: Transition {
            enabled: Config.animations
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: 250
            }

        }

        exit: Transition {
            enabled: Config.animations
            NumberAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: 250
            }

        }

    }

    SystemClock {
        id: clock

        precision: SystemClock.Seconds
    }
}
