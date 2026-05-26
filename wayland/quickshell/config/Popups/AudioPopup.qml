import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Services.Pipewire
import qs
import qs.Common
import qs.Services

DetailsPopup {
    id: root

    height: container.height
    width: Config.em(14)
    property list<PwNode> programs: []

    PwObjectTracker {
        objects: programs
    }

    Column {
        id: container

        spacing: 4

        VolumeControl {
            device: Pipewire.defaultAudioSink
            isPrimary: true
        }

        Repeater {

            model: ScriptModel {
                values: Pipewire.linkGroups.values.filter(function(group) {
                    return group.target === Pipewire.defaultAudioSink;
                }).map(function(group) {
                    return group.source;
                })
            }

            delegate: VolumeControl {
                required property PwNode modelData

                device: modelData
            }

        }

        Rectangle {
            color: U.rgba(250, 250, 250, 0.6)
            height: 2
            width: root.width - 20
            x: 10
            y: 2
        }

        VolumeControl {
            device: Pipewire.defaultAudioSource
            isPrimary: true
        }

    }

    component VolumeControl: Rectangle {
        id: control

        property PwNode device
        property bool isPrimary: false

        color: "transparent"
        implicitHeight: muteButton.height
        implicitWidth: root.width
        visible: device.audio != null

        Component.onCompleted: {
            root.programs.push(device)
        }

        Rectangle {
            id: muteButton

            property bool hover: false
            property bool isMuted: control.device.audio ? control.device.audio.muted : false

            color: hover ? U.rgba(100, 100, 100, 0.8) : U.rgba(100, 100, 100, 0.4)
            height: Config.em(1.7)
            width: Config.em(1.7)
            radius: 6

            Text {
                id: muteIcon

                color: {
                    if (!muteButton.isMuted)
                        return muteButton.hover ? U.rgba(10, 10, 10, 1) : U.rgba(255, 255, 255, 1);

                    return muteButton.hover ? U.rgba(255, 255, 255, 1) : U.rgba(10, 10, 10, 1);
                }
                font.pixelSize: Config.em(1.6)
                text: {
                    if (control.device.isSink && muteButton.isMuted)
                        return muteButton.hover ? "󰕾" : "󰸈";

                    if (control.device.isSink)
                        return muteButton.hover ? "󰸈" : "󰕾";

                    if (muteButton.isMuted)
                        return muteButton.hover ? "󰍬" : "󰍭";
                    else
                        return muteButton.hover ? "󰍭" : "󰍬";
                }
                x: Config.em(0.45)
                y: -Config.em(0.3)
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    control.device.audio.muted = !control.device.audio.muted;
                }
                onEntered: {
                    muteButton.hover = true;
                }
                onExited: {
                    muteButton.hover = false;
                }
            }

        }

        Slider {
            id: slider

            from: 0
            hoverEnabled: true
            to: 1.5
            value: control.device.audio.volume
            width: control.width - x
            x: Config.em(1.9)

            onMoved: {
                control.device.audio.volume = value;
            }

            background: Rectangle {
                color: slider.hovered ? U.rgba(200, 200, 200, 1) : U.rgba(200, 200, 200, 0.5)
                height: Config.em(0.6)
                radius: Config.em(0.3)
                y: Config.em(0.6)

                Behavior on color {
                    enabled: Config.animations
                    ColorAnimation {
                        duration: 150
                    }
                }

                Rectangle {
                    color: {
                        if (control.device.audio.muted)
                            return slider.hovered ? U.rgba(90, 90, 90, 1) : U.rgba(40, 40, 40, 1)

                        return slider.hovered ? U.rgba(24, 186, 210, 1.0) : U.rgba(24, 120, 130, 1.0)
                    }
                    height: slider.hovered ? Config.em(1.0) : parent.height + 2
                    radius: parent.radius * 2
                    width: parent.width * slider.visualPosition
                    y: slider.hovered ? -Config.em(0.2) : -1

                    Behavior on color {
                        enabled: Config.animations
                        ColorAnimation {
                            duration: 150
                        }
                    }
                    Behavior on height {
                        enabled: Config.animations
                        NumberAnimation {
                            duration: 150
                        }
                    }
                    Behavior on y {
                        enabled: Config.animations
                        NumberAnimation {
                            duration: 150
                        }
                    }
                }
            }

            handle: Rectangle {
                color: U.rgba(0, 0, 0, 0.0)
                implicitHeight: Config.em(1.2)
                implicitWidth: Config.em(1.2)
                radius: Config.em(0.3)
                x: slider.visualPosition * slider.background.width - width + Config.em(0.2)
                y: Config.em(0.3)
            }

            MouseArea {
                acceptedButtons: Qt.NoButton
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
            }
        }

        Text {
            color: control.device.audio.muted ? U.rgba(240, 240, 240, 1) : U.rgba(44, 44, 44, 1)
            font.pixelSize: Config.em(0.7)
            font.weight: control.isPrimary ? 700 : 400
            text: control.device.nickname ? control.device.nickname : (control.device.description ? control.device.description : control.device.name)
            x: Config.em(2.1)
            y: Config.em(0.4)

            Behavior on color {
                enabled: Config.animations
                ColorAnimation {
                    duration: 100
                }
            }
        }

    }

}
