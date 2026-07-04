import QtQuick
import qs

Rectangle {
    id: root

    required property bool enabled
    required property string icon
    property bool hovered: false
    required property var onClicked

    border.color: enabled ? U.rgba(0, 185, 155, 0.8) : U.rgba(255, 255, 255, 0.4)
    border.width: 3
    color: {
        if (hovered)
            return U.rgba(255, 255, 255, 0.8);
        return enabled ? U.rgba(0, 185, 255, 0.8) : U.rgba(255, 255, 255, 0.1);
    }
    height: Config.em(2.4)
    radius: 15
    width: Config.em(2.4)

    Behavior on color {
        enabled: Config.animations
        ColorAnimation {
            target: root
            duration: 200
        }
    }

    Behavior on border.color {
        enabled: Config.animations
        ColorAnimation {
            target: root
            duration: 200
        }
    }

    Text {
        anchors.fill: parent
        color: {
            if (hovered)
                return U.rgba(0, 0, 0, 1);
            return enabled ? U.rgba(0, 0, 0, 1) : U.rgba(155, 155, 155, 1);
        }
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: Config.em(1.4)
        text: icon
        verticalAlignment: Text.AlignVCenter

        Behavior on color {
            enabled: Config.animations
            ColorAnimation {
                duration: 200
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onEntered: hovered = true
        onExited: hovered = false
        onClicked: function (e) {
            root.onClicked();
        }
    }
}
