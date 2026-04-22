import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Services.SystemTray
import qs

Row {
    id: container
    y: parent.topPadding + 2
    x: 4
    visible: isPrimary
    width: childrenRect.width + 8

    component TrayIcon: Rectangle {
        id: root

        color: "Transparent"
        height: icon.height
        width: icon.width

        Image {
            id: icon
            source: modelData.icon

            height: Config.em(1)
            smooth: true
            width: Config.em(1)
        }

        MouseArea {
            id: cursor

            property bool hovered: false
            acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: {
                if (modelData.tooltipTitle && modelData.tooltipTitle.length > 0)
                    return true
                if (modelData.tooltipDescription && modelData.tooltipDescription.length > 0)
                    return true
                return false
            }

            onEntered: { hovered = true }
            onExited: { hovered = false }

            onClicked: function(event) {
                if (event.button === Qt.LeftButton) {
                    if (modelData.onlyMenu)
                        return openMenu(event)
                    return modelData.activate()
                } else if (event.button === Qt.RightButton) {
                    return openMenu(event)
                } else {
                    return modelData.secondaryActivate();
                }
            }
        }

        ToolTip {
            id: tooltip

            delay: 500
            padding: 4
            popupType: Popup.Native
            visible: cursor.hovered
            y: 1.5 * root.height

            contentItem: Text {
                text: {
                    if (!modelData.tooltipTitle || modelData.tooltipTitle.length === 0)
                        return modelData.tooltipDescription ? modelData.tooltipDescription : "";
                    if (modelData.tooltipDescription && modelData.tooltipDescription.length > 0)
                        return `${modelData.tooltipTitle} - ${modelData.tooltipDescription}`;
                    return modelData.tooltipTitle
                }

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

        function openMenu(event) {
            menu.active ? menu.close() : menu.open();
        }

        QsMenuAnchor {
            id: menu
            anchor {
                window: bar
                item: root
                edges: Edges.Bottom
            }

            menu: modelData.menu
        }
    }

    Repeater {
        model: SystemTray.items.values

        TrayIcon {
            required property SystemTrayItem modelData;
        }
    }
}
