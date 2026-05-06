import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Quickshell
import Quickshell.Hyprland
import Quickshell.Services.Notifications
import Quickshell.Wayland
import qs
import qs.Common
import qs.Services

Variants {
    model: Quickshell.screens

    delegate: Component {
        PanelWindow {
            id: root

            required property var modelData
            property var screen: modelData
            property bool isFocused: Hyprland.monitorFor(modelData).focused
            property bool isEmpty: true
            property ListModel inbox

            WlrLayershell.namespace: "quickshell::notifications"
            color: "transparent"
            exclusionMode: ExclusionMode.Ignore
            implicitHeight: listView.height
            implicitWidth: Config.em(18)
            margins.top: Config.em(2.5)
            visible: !isEmpty
            Component.onCompleted: {
                inbox = NotificationService.getOutput(screen.name);
            }

            ListModel {
                id: notifications
            }

            anchors {
                top: true
                right: true
                bottom: true
            }

            Connections {
                function onCountChanged() {
                    if (inbox.count === 0)
                        return ;

                    isEmpty = false;
                    var payload = inbox.get(0);
                    if (payload.action === "add") {
                        notifications.append(payload.msg);
                    } else if (payload.action === "remove") {
                        var idx = -1;
                        for (var i = 0; i < notifications.count; i++) {
                            if (notifications.get(i).id === payload.target) {
                                idx = i;
                                break;
                            }
                        }
                        if (idx > -1) {
                            notifications.remove(idx, 1);
                        } else {
                            var available = "";
                            for (var i = 0; i < notifications.count; i++) {
                                if (available.length === 0)
                                    available = `${notifications.get(i).id}`;
                                else
                                    available = `${available},${notifications.get(i).id}`;
                            }
                        }
                    } else {
                        console.log(`Unknown action: ${payload.action}`);
                    }
                    inbox.clear();
                }

                target: inbox
            }

            ListView {
                id: listView

                height: contentHeight
                spacing: 10
                model: notifications

                anchors {
                    left: parent.left
                    right: parent.right
                    rightMargin: Config.em(0.5)
                }

                add: Transition {
                    NumberAnimation {
                        property: "x"
                        from: 400
                        to: 0
                        duration: 400
                    }

                }

                remove: Transition {
                    ParallelAnimation {
                        onFinished: {
                            if (notifications.count === 0)
                                isEmpty = true;

                        }

                        NumberAnimation {
                            property: "y"
                            to: -300
                            duration: 400
                        }

                        NumberAnimation {
                            property: "opacity"
                            to: 0
                            duration: 300
                        }

                    }

                }

                displaced: Transition {
                    NumberAnimation {
                        property: "y"
                        duration: 1400
                    }

                }

                delegate: Rectangle {
                    id: container

                    required property var model
                    required property int index
                    property bool isRemoved: false

                    color: "transparent"
                    implicitHeight: base.height
                    implicitWidth: listView.width

                    NotificationPopup {
                        id: base

                        modelData: model
                        width: container.implicitWidth
                        color: U.rgba(120, 120, 120, 0.3)
                    }

                }

            }

            // An empty click mask prevents the window from blocking mouse events.
            mask: Region {
                item: listView
            }

        }

    }

}
