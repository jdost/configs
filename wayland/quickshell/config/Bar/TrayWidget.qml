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
    width: childrenRect.width + Config.em(0.05)

    Repeater {
        model: SystemTray.items.values

        TrayIcon {
            required property SystemTrayItem modelData
        }

    }

    component TrayIcon: Rectangle {
        id: root

        function openMenu(event) {
            menu.active ? menu.close() : menu.open();
        }

        color: "Transparent"
        height: icon.height
        width: icon.width + Config.em(0.15)

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
                    return true;

                if (modelData.tooltipDescription && modelData.tooltipDescription.length > 0)
                    return true;

                return false;
            }
            onEntered: {
                hovered = true;
            }
            onExited: {
                hovered = false;
            }
            onClicked: function(event) {
                if (event.button === Qt.LeftButton) {
                    if (modelData.onlyMenu)
                        return openMenu(event);

                    return modelData.activate();
                } else if (event.button === Qt.RightButton) {
                    return openMenu(event);
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

                    return modelData.tooltipTitle;
                }
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

        QsMenuAnchor {
            id: menu

            menu: modelData.menu

            anchor {
                window: bar
                item: root
                edges: Edges.Bottom
            }

        }

    }

}
