import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Bluetooth
import Quickshell.Widgets
import qs
import qs.Common

DetailsPopup {
    id: root

    property int iconSize: Config.em(1.5)

    width: Config.em(15)
    height: container.height

    Column {
        id: container

        spacing: 8

        RowLayout {
            id: controller

            spacing: 6
            width: root.width

            DeviceIcon {
                name: 'bluetoothradio'
            }

            Text {
                Layout.fillWidth: true
                color: U.rgba(220, 220, 220, 0.9)
                font.pixelSize: Config.em(1)
                text: Bluetooth.defaultAdapter ? `Controller: ${Bluetooth.defaultAdapter.name}` : ""
            }

            Button {
                function onClicked() {
                    Bluetooth.defaultAdapter.enabled = !Bluetooth.defaultAdapter.enabled;
                }

                text: (Bluetooth.defaultAdapter && Bluetooth.defaultAdapter.enabled) ? "Disable" : "Enable"
            }
        }

        Rectangle {
            color: "transparent"
            height: 6
            width: root.width

            Rectangle {
                color: U.rgba(250, 250, 250, 0.6)
                height: 2
                width: root.width - 20
                x: 10
                y: 2
            }
        }

        Repeater {
            model: Bluetooth.devices

            RowLayout {
                id: device

                required property BluetoothDevice modelData

                spacing: 4
                width: root.width

                DeviceIcon {
                    name: modelData.icon
                }

                Text {
                    Layout.fillWidth: true
                    color: U.rgba(220, 220, 220, 0.9)
                    font.pixelSize: Config.em(1)
                    text: modelData.name
                }

                Button {
                    function onClicked() {
                        // Enable the controller if trying to connect
                        if (!Bluetooth.defaultAdapter.enabled)
                            Bluetooth.defaultAdapter.enabled = true;

                        if (modelData.connected)
                            modelData.disconnect();
                        else
                            modelData.connect();
                    }

                    text: modelData.connected ? "Disconnect" : "Connect"
                }
            }
        }
    }

    component DeviceIcon: IconImage {
        property string name

        implicitSize: root.iconSize
        source: Quickshell.iconPath(name)
    }

    component Button: Rectangle {
        id: base

        property string text
        property bool hover: false

        function onClicked() {
        }

        color: hover ? U.rgba(200, 200, 200, 0.8) : U.rgba(200, 200, 200, 0.4)
        implicitHeight: contents.height + 4
        implicitWidth: contents.width + 8
        radius: 6

        Text {
            id: contents

            font.pixelSize: Config.em(0.9)
            color: U.rgba(255, 255, 255, 1)
            text: base.text
            x: 4
            y: 2
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: {
                base.onClicked();
            }
            onEntered: {
                base.hover = true;
            }
            onExited: {
                base.hover = false;
            }
        }
    }
}
