import QtQuick
import Quickshell
import qs

Rectangle {
    id: icons

    color: Qt.rgba(200 / 255, 200 / 255, 200 / 255, 0.25)
    radius: Config.em(3)
    implicitHeight: childrenRect.height + Config.em(0.3)
    implicitWidth: childrenRect.width
    visible: isPrimary
    y: parent.topPadding

    Row {
        leftPadding: Config.em(0.6)
        rightPadding: Config.em(0.6)
        spacing: 5

        VideoCaptureIcon {
        }

        AudioCaptureIcon {
        }

        AudioIcon {
        }

        BatteryIcon {
        }

        BluetoothIcon {
        }

        NetworkIcon {
        }

        MprisIcon {
        }

        CpuIcon {
        }

        MemoryIcon {
        }

    }

}
