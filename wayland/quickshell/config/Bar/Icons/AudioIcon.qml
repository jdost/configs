import QtQuick
import QtQuick.Controls
import Quickshell
import qs
import qs.Popups
import qs.Services

Item {
    id: base

    implicitHeight: Config.em(1)
    implicitWidth: Config.em(0.5)
    visible: isPrimary && Config.enabled("audio")

    Row {
        spacing: 0

        Repeater {
            model: [{
                "volume": VolumeService.outputVolume,
                "isMuted": VolumeService.outputIsMuted
            }, {
                "volume": VolumeService.inputVolume,
                "isMuted": VolumeService.inputIsMuted
            }]

            delegate: Column {
                id: container

                required property var modelData
                property real volume: modelData.volume
                property bool isMuted: modelData.isMuted
                readonly property color muteColor: U.rgb(120, 120, 120)

                height: Config.em(0.8)
                spacing: 3
                topPadding: Config.em(0.2)
                width: childrenRect.width + 3

                Repeater {
                    id: levelDots

                    model: [{
                        "max": 1,
                        "color": U.rgb(0, 255, 0)
                    }, {
                        "max": 0.75,
                        "color": U.rgb(255, 255, 0)
                    }, {
                        "max": 0.5,
                        "color": U.rgb(255, 102, 0)
                    }, {
                        "max": 0.25,
                        "color": U.rgb(255, 0, 0)
                    }]

                    delegate: Rectangle {
                        required property var modelData

                        color: {
                            if (isMuted)
                                return muteColor;

                            if ((modelData.max - 0.25) === 0 && volume === 0)
                                return muteColor;

                            if (volume <= (modelData.max - 0.25))
                                return U.rgb(153, 153, 153);

                            return modelData.color;
                        }
                        opacity: {
                            if (isMuted)
                                return 1;

                            if (volume >= modelData.max)
                                return 1;

                            if (volume <= (modelData.max - 0.25))
                                return 1;

                            return (volume - (modelData.max - 0.25)) * 4;
                        }
                        height: Config.em(0.12)
                        radius: 10
                        width: Config.em(0.12)
                    }

                }

            }

        }

    }

    MouseArea {
        id: mouse

        anchors.fill: base
        hoverEnabled: true
        onClicked: {
            tooltip.visible = popup.shown;
            popup.toggle();
        }
        onEntered: {
            tooltip.visible = true;
        }
        onExited: {
            tooltip.visible = false;
        }
    }

    AudioPopup {
        id: popup

        timeout: 10000
    }

    ToolTip {
        id: tooltip

        delay: 500
        padding: 4
        popupType: Popup.Native
        y: Config.em(1.5)

        contentItem: Text {
            text: {
                if (VolumeService.outputIsMuted)
                    return "Volume: Muted";

                return `Volume: ${(VolumeService.outputVolume * 100).toFixed(2)}%`;
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
                from: 0
                to: 1
                duration: 250
            }

        }

        exit: Transition {
            NumberAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: 250
            }

        }

    }

}
