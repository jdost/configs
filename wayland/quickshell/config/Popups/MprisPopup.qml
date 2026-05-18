import QtQuick
import Quickshell.Widgets
import qs
import qs.Common

DetailsPopup {
    id: popup

    property var player

    timeout: 10000
    height: 72 + 10

    Rectangle {
        id: container

        IconImage {
            id: cover

            implicitSize: 72
            y: 5
            source: popup.player ? popup.player.trackArtUrl : ""
        }

        Rectangle {
            id: trackTitle

            height: Config.em(1.25)
            width: popup.width - 84
            x: 80
            y: Config.em(0.1)
            color: "transparent"
            clip: true

            Text {
                color: U.rgba(255, 255, 255, 1)
                font.pixelSize: Config.em(1.1)
                text: popup.player ? popup.player.trackTitle : ""
            }

        }

        Rectangle {
            id: trackArtist

            anchors.fill: parent
            anchors.leftMargin: 80
            anchors.topMargin: Config.em(1.3)

            Text {
                color: U.rgba(200, 200, 200, 1)
                font.pixelSize: Config.em(0.9)
                text: popup.player ? popup.player.trackArtist : ""
            }

        }

        Row {
            id: controls

            x: 72 + ((popup.width - childrenRect.width - 72) / 2)
            y: Config.em(2.5)

            ControlButton {
                id: previousTrack

                function trigger() {
                    popup.player.previous();
                }

                icon: ""
                visible: popup.player ? popup.player.canGoPrevious : false
            }

            ControlButton {
                id: playPause

                function trigger() {
                    popup.player.togglePlaying();
                }

                icon: {
                    if (!popup.player)
                        return "";

                    if (popup.player.isPlaying)
                        return "";

                    return "";
                }
            }

            ControlButton {
                id: nextTrack

                function trigger() {
                    popup.player.next();
                }

                icon: ""
                visible: popup.player ? popup.player.canGoNext : false
            }

        }

        component ControlButton: Rectangle {
            id: root

            property bool hover: false
            property string icon

            function trigger() {
            }

            color: hover ? U.rgba(200, 200, 200, 0.4) : U.rgba(200, 200, 200, 0)
            implicitWidth: Config.em(1.4) + 4
            implicitHeight: Config.em(1.4) + 4
            radius: 6

            Text {
                y: 2 - Config.em(0.75)
                x: 2 + Config.em(0.2)
                font.pixelSize: Config.em(2)
                color: U.rgba(255, 255, 255, 1)
                text: icon
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    root.trigger();
                }
                onEntered: {
                    hover = true;
                }
                onExited: {
                    hover = false;
                }
            }

            Behavior on color {
                ColorAnimation {
                    duration: 150
                }

            }

        }

    }

}
