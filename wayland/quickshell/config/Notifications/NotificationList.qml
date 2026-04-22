import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import Quickshell.Hyprland
import Quickshell.Services.Notifications
import qs
import qs.Services
import qs.Common

Variants {
    model: Quickshell.screens

    delegate: Component {
        PanelWindow {
            id: root
            WlrLayershell.namespace: "quickshell::notifications"

            readonly property real defaultTimeout: 5000;
            required property var modelData
            property var screen: modelData
            property bool isFocused: Hyprland.monitorFor(modelData).focused
            property bool isEmpty: true
            property ListModel inbox

            // An empty click mask prevents the window from blocking mouse events.
            mask: Region {
                item: listView
            }

            ListModel {
                id: notifications
            }

            anchors {
                top: true
                right: true
                bottom: true
            }

            color: "transparent";
            exclusionMode: ExclusionMode.Ignore;
            implicitHeight: listView.height;
            implicitWidth: Config.em(18.0);
            margins.top: Config.em(2.5);
            visible: !isEmpty;

            Component.onCompleted: {
                inbox = NotificationService.getOutput(screen.name)
            }

            Connections {
                target: inbox
                function onCountChanged() {
                    if (inbox.count === 0)
                        return;

                    isEmpty = false
                    notifications.append(inbox.get(0).msg)
                    inbox.clear()
                }
            }

            ListView {
                id: listView

                height: contentHeight
                spacing: 10

                anchors {
                    left: parent.left;
                    right: parent.right;
                    rightMargin: Config.em(0.5)
                }

                add: Transition {
                    NumberAnimation { property: "x"; from: 400; to: 0; duration: 400 }
                }

                remove: Transition {
                    ParallelAnimation {
                        NumberAnimation { property: "y"; to: -300; duration: 400 }
                        NumberAnimation { property: "opacity"; to: 0.0; duration: 300 }

                        onFinished: {
                            if (notifications.count === 0)
                                isEmpty = true
                        }
                    }
                }

                displaced: Transition {
                    NumberAnimation { property: "y"; duration: 1400 }
                }

                model: notifications;

                delegate: Rectangle {
                    required property var model;
                    required property int index;
                    id: container

                    color: "transparent"
                    implicitHeight: base.height
                    implicitWidth: listView.width

                    NotificationPopup {
                        modelData: model

                        id: base
                        width: container.implicitWidth
                        color: U.rgba(120, 120, 120, 0.3)
                    }

                    Timer {
                        interval: model.expireTimeout > 0 ? model.expireTimeout : defaultTimeout;
                        repeat: false;
                        running: true;

                        onTriggered: function () {
                            listView.model.remove(index, 1);
                            NotificationService.expirePopup(model.id);
                        }
                    }
                }
            }
        }
    }
}
