import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Services.Notifications

import qs
import qs.Common
import qs.Services

Rectangle {
    id: root

    anchors.fill: parent
    color: "transparent"

    Row {
        id: controls

        width: root.width - Config.em(0.4)
        height: childrenRect.height
        spacing: 15

        Rectangle {
            color: "transparent"
            height: Config.em(1)
            anchors.verticalCenter: dndButton.verticalCenter
            width: controls.width - dndButton.width - clearButton.width - 2 * controls.spacing

            Text {
                color: "white"
                font.pixelSize: Config.em(0.8)
                text: "Notifications"
                x: Config.em(1.4)
            }
        }

        Rectangle {
            id: dndButton

            property bool hovered: false

            border {
                color: U.rgba(255, 255, 255, 0.7)
                width: NotificationService.dnd ? 2 : 0
            }
            color: hovered ? U.rgba(245, 245, 245, 0.5) : U.rgba(245, 245, 245, 0.2)
            height: Config.em(1.4)
            radius: Config.em(0.3)
            width: Config.em(1.4)
            y: Config.em(0.2)

            Text {
                color: "white"
                font.pixelSize: Config.em(1.2)
                text: "󰂛"
                x: Config.em(0.4)
                y: -Config.em(0.1)
            }

            ToolTip {
                delay: 150
                padding: 4
                popupType: Popup.Native
                visible: dndButton.hovered
                y: Config.em(0.5)

                contentItem: Text {
                    color: U.rgba(212, 212, 212, 1)
                    font.pixelSize: Config.em(0.5)
                    text: "Toggle DND"
                }

                background: Rectangle {
                    color: U.rgba(17, 17, 17, 0.3)
                    radius: 15
                }
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true

                onClicked: {
                    NotificationService.dnd = !NotificationService.dnd;
                }
                onEntered: {
                    parent.hovered = true;
                }
                onExited: {
                    parent.hovered = false;
                }
            }
        }

        Rectangle {
            id: clearButton

            property bool hovered: false

            color: hovered ? U.rgba(245, 245, 245, 0.5) : U.rgba(245, 245, 245, 0.2)
            height: Config.em(1.4)
            radius: Config.em(0.3)
            width: Config.em(1.4)
            y: Config.em(0.2)

            Text {
                color: "white"
                font.pixelSize: Config.em(1.2)
                text: "󰱢"
                x: Config.em(0.4)
                y: -Config.em(0.1)
            }

            ToolTip {
                delay: 150
                padding: 4
                popupType: Popup.Native
                visible: clearButton.hovered
                y: Config.em(0.5)

                contentItem: Text {
                    color: U.rgba(212, 212, 212, 1)
                    font.pixelSize: Config.em(0.5)
                    text: "Clear History"
                }

                background: Rectangle {
                    color: U.rgba(17, 17, 17, 0.3)
                    radius: 15
                }
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true

                onClicked: {
                    if (NotificationService.current.length === 0)
                        return;
                    NotificationService.dismissAll();
                }
                onEntered: {
                    parent.hovered = true;
                }
                onExited: {
                    parent.hovered = false;
                }
            }
        }
    }

    Column {
        id: history

        anchors {
            fill: parent
            leftMargin: Config.em(0.4)
            rightMargin: Config.em(0.4)
            topMargin: Config.em(1.2)
        }
        spacing: 10

        Component.onCompleted: {
            console.log(NotificationService.current.length);
        }

        Repeater {
            model: NotificationService.current.length

            Rectangle {
                id: container

                required property real index
                property Notification notification: NotificationService.current[index]

                color: "transparent"
                implicitHeight: base.height
                implicitWidth: history.width - Config.em(0.2)
                x: Config.em(0.1)

                NotificationPopup {
                    id: base

                    color: U.rgba(120, 120, 120, 0.1)
                    modelData: container.notification
                    width: container.implicitWidth

                    MouseArea {
                        acceptedButtons: Qt.RightButton
                        anchors.fill: parent
                        onClicked: {
                            container.notification.dismiss();
                        }
                    }
                }
            }
        }
    }
}
