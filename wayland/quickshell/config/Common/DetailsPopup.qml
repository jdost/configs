pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import qs

Scope {
    id: popup

    property bool shown: false;
    default property list<QtObject> content
    property int height: Config.em(6);
    property int padding: Config.em(0.5);
    property int timeout: 5000;
    property int width: Config.em(18);

    function toggle() {
        if (shown) {
            loader.y = loader.slideUpPos;
        } else {
            loader.active = true;
            loader.y = 0;
        }
        shown = !shown;
    }

    LazyLoader {
        id: loader
        property int slideUpPos: 0 - popup.padding*2 - popup.height;
        property int y: slideUpPos;

        PanelWindow {
            id: window

            anchors {
                top: true
                right: true
            }

            color: "transparent";
            implicitHeight: popup.height + popup.padding*2;
            implicitWidth: popup.width + popup.padding*2;
            margins.right: Config.em(0.5);
            margins.top: Config.em(0.3);
            WlrLayershell.namespace: "quickshell::popup"

            Timer {
                id: hideTimeout

                interval: popup.timeout
                repeat: false
                running: !mouseDetector.containsMouse

                onTriggered: function () {
                    if (popup.shown)
                        popup.toggle();
                }
            }

            MouseArea {
                id: mouseDetector
                // This isn't great, it get's overlapped with other mouseareas, but it still
                // does an okay job of blocking timeouts when hovered
                acceptedButtons: Qt.NoButton
                anchors.fill: parent
                hoverEnabled: true
            }

            Rectangle {
                id: background

                radius: Config.em(0.75)
                implicitHeight: popup.padding*2 + popup.height;
                implicitWidth: popup.padding*2 + popup.width;
                color: U.rgba(50, 50, 50, 0.4)
                y: loader.y;

                onYChanged: function () {
                    if (y === loader.slideUpPos && !popup.shown) {
                        loader.active = false;
                    }
                }

                Behavior on y {
                    enabled: Config.animations
                    SmoothedAnimation {
                        velocity: 450;
                    }
                }

                Rectangle {
                    id: content

                    color: "transparent";
                    data: popup.content;
                    height: popup.height;
                    width: popup.width;
                    x: popup.padding;
                    y: popup.padding;
                }
            }
        }

    }

}
