import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications
import qs
import qs.Services

Rectangle {
    required property var modelData;
    property real padding: Config.em(0.5);

    id: popup
    radius: Config.em(0.75)
    implicitHeight: container.height + padding*2

    Row {
        id: container
        height: Math.max(content.height, icon.height) + popup.padding
        y: popup.padding
        x: popup.padding
        spacing: 10

        IconImage {
            id: icon

            source: {
                if (modelData.image)
                    return modelData.image
                if (modelData.appIcon)
                    return Quickshell.iconPath(modelData.appIcon)
                return Quickshell.iconPath("dialog-information-symbolic");
            }
            y: 5
            implicitSize: Config.em(2.2)
        }

        Column {
            id: content
            y: 0
            width: popup.width - icon.implicitSize - 2*popup.padding - container.spacing*2;
            height: summary.height + body.height + actionsContainer.height

            Text {
                id: summary
                clip: true
                text: modelData.summary
                width: content.width

                anchors.leftMargin: Config.em(0.1)

                color: U.rgba(250, 250, 250, 1.0);
                font.pixelSize: Config.em(0.9)
                font.bold: true
            }

            Text {
                id: body
                maximumLineCount: 8
                text: modelData.body
                width: content.width
                wrapMode: Text.Wrap

                color: U.rgba(250, 250, 250, 1.0);
                font.pixelSize: Config.em(0.8)
            }


            Rectangle {
                id: actionsContainer
                visible: {
                    if (modelData.appName === "WebCord")
                        return false
                    return modelData.actions.count > 0
                }
                height: visible ? Config.em(1.6) + 10 : 0
                width: content.width
                color: "transparent"

                RowLayout {
                    id: actions
                    y: 10
                    height: Config.em(1.6)
                    width: content.width

                    Repeater {
                        model: modelData.actions

                        Rectangle {
                            required property var modelData
                            required property real index
                            property bool hover: false
                            id: button

                            Layout.fillWidth: true
                            height: actions.height
                            radius: Config.em(0.2)
                            color: hover ? U.rgba(200, 200, 200, 0.7) : U.rgba(200, 200, 200, 0.3);

                            Text {
                                anchors.fill: parent
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter

                                color: "white"
                                font.pixelSize: Config.em(1.0)
                                text: modelData.text
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    NotificationService.invokeAction(popup.modelData.id, modelData.identifier);
                                }
                                onEntered: button.hover = true
                                onExited: button.hover = false
                            }
                        }
                    }
                }
            }
        }
    }
}
