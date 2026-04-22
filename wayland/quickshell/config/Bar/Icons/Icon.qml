import QtQuick
import QtQuick.Controls
import qs

Item {
    id: base

    property string icon: "?"
    property color iconColor: U.rgba(0, 255, 0, 1)
    property string module: ""
    property real size: Config.em(1)
    property string tooltip: ""
    property int topPadding: -2

    implicitHeight: Config.em(1)
    implicitWidth: icon.width
    visible: isPrimary && Config.enabled(module)

    Text {
        id: icon

        antialiasing: false
        color: base.iconColor
        font.pixelSize: base.size
        text: base.icon
        topPadding: (Config.em(1) - base.size) + base.topPadding

        MouseArea {
            id: mouse

            anchors.fill: base.tooltip != "" ? icon : null
            hoverEnabled: true
            onEntered: {
                tooltip.visible = true;
            }
            onExited: {
                tooltip.visible = false;
            }
        }

        ToolTip {
            id: tooltip

            delay: 500
            padding: 4
            popupType: Popup.Native
            y: Config.em(1.5)

            contentItem: Text {
                text: base.tooltip
                color: U.rgba(17, 17, 17, 1)
                font.pixelSize: Config.em(0.7)
            }

            background: Rectangle {
                radius: 15
                color: U.rgba(212, 212, 212, 0.65)
            }

            enter: Transition {
                NumberAnimation {
                    property: "opacity"
                    from: 0.0
                    to: 1.0
                    duration: 250
                }
            }

            exit: Transition {
                NumberAnimation {
                    property: "opacity"
                    from: 1.0
                    to: 0.0
                    duration: 250
                }
            }
        }

    }

}
