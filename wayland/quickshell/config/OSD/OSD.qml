import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Widgets
import qs
import qs.Services

Scope {
	id: root

    property bool isVisible: false
    property real hideTimeout: 2000
    property real level: 0.5;
    property bool isLoading: true;
    property bool isMuted: false
    property bool isVolume: true

    Timer {
        id: loadingTimer
        interval: 500;
        running: true;

        onTriggered: root.isLoading = false
    }

	Timer {
        id: displayTimer
        interval: hideTimeout
        onTriggered: root.isVisible = false
	}

    Connections {
        target: VolumeService

        function onOutputVolumeChanged () {
            if (isLoading)
                return;
            isVolume = true;
            isVisible = true;
            level = Qt.binding(() => VolumeService.outputVolume);
            isMuted = Qt.binding(() => VolumeService.outputIsMuted);

            displayTimer.restart();
        }
        function onOutputIsMutedChanged () {
            if (isLoading)
                return;
            isVolume = true;
            isVisible = true;
            level = Qt.binding(() => VolumeService.outputVolume);
            isMuted = Qt.binding(() => VolumeService.outputIsMuted);

            displayTimer.restart();
        }
    }

    Connections {
        target: BrightnessService

        function onLevelChanged () {
            if (isLoading)
                return;
            isVolume = false;
            isVisible = true;
            level = Qt.binding(() => BrightnessService.level);
            isMuted = false;

            displayTimer.restart();
        }
    }

	LazyLoader {
	    active: root.isVisible

        PanelWindow {
            anchors.bottom: true
            margins.bottom: Config.em(1.5)
            exclusiveZone: 0

            implicitWidth: contents.implicitWidth + 2*Config.em(2.0)
            implicitHeight: contents.implicitHeight + 2*Config.em(1.0)
            color: "transparent"

            // An empty click mask prevents the window from blocking mouse events.
            mask: Region {}

            Rectangle {
                id: contents
                anchors {
                    fill: parent
                    bottomMargin: Config.em(1.0)
                    leftMargin: Config.em(2.0)
                    rightMargin: Config.em(2.0)
                    topMargin: Config.em(1.0)
                }
                implicitWidth: Config.em(15.0)
                implicitHeight: Config.em(2.0)

                radius: Config.em(2.2)
                color: U.rgba(34, 34, 34, 0.6);

                RowLayout {
                    spacing: 10
                    anchors {
                        fill: parent
                        leftMargin: Config.em(0.5)
                        rightMargin: Config.em(1.0)
                    }

                    IconImage {
                        mipmap: true
                        implicitSize: Config.em(1.5)
                        source: {
                            if (isVolume && isMuted)
                                return Quickshell.iconPath(`audio-volume-muted-symbolic`);

                            var level = isVolume ? "muted" : "off"
                            if (root.level > 0.66)
                                level = "high"
                            else if (root.level > 0.34)
                                level = "medium"
                            else if (root.level > 0)
                                level = "low"

                            if (isVolume) {
                                return Quickshell.iconPath(`audio-volume-${level}-symbolic`);
                            } else {
                                return Quickshell.iconPath(`display-brightness-${level}-symbolic`);
                            }
                        }
                    }

                    Rectangle {
                        id: trough

                        color: U.rgba(125, 125, 125, 0.6);
                        implicitHeight: Config.em(0.8)
                        Layout.fillWidth: true
                        radius: Config.em(2.0)

                        Rectangle {
                            id: fill

                            implicitWidth: parent.width * root.level
                            radius: parent.radius

                            anchors {
                                left: parent.left
                                top: parent.top
                                bottom: parent.bottom
                                margins: 3;
                            }

                            color: {
                                if (isVolume && isMuted)
                                    return U.rgba(34, 34, 34, 0.75)
                                return U.rgba(255, 255, 255, 0.75)
                            }

                            Behavior on implicitWidth {
                                NumberAnimation {
                                    duration: 150
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
