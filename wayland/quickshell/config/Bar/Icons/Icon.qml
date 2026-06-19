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
    property bool tooltipEnabled: base.tooltip.length > 0
    property int topPadding: -2
    property var onClicked

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
                if (tooltip.isEnabled)
                    tooltip.visible = true;
            }
            onExited: {
                if (tooltip.isEnabled)
                    tooltip.visible = false;
            }
            onClicked: {
                if (base.onClicked) {
                    base.onClicked();
                }
            }
        }

        ToolTip {
            id: tooltip

            property bool isEnabled: base.tooltipEnabled

            onIsEnabledChanged: function () {
                if (!isEnabled)
                    tooltip.visible = false;
            }
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
    }
}
