pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Quickshell
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
        console.log("toggled");
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

            implicitHeight: popup.height + popup.padding*2;
            implicitWidth: popup.width + popup.padding*2;
            margins.top: Config.em(0.3);
            margins.right: Config.em(0.5);
            color: "transparent";

            Timer {
                interval: popup.timeout
                repeat: false
                running: true

                onTriggered: function () {
                    if (popup.shown)
                        popup.toggle();
                }
            }

            Rectangle {
                id: background

                radius: Config.em(0.75)
                implicitHeight: popup.padding*2 + popup.height;
                implicitWidth: popup.padding*2 + popup.width;
                color: U.rgba(100, 100, 100, 0.4)
                y: loader.y;

                onYChanged: function () {
                    if (y === loader.slideUpPos && !popup.shown) {
                        loader.active = false;
                    }
                }

                Behavior on y {
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
