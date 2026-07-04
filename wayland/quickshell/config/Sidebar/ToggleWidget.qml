import QtQuick
import QtQuick.Layouts
import qs
import qs.Sidebar.Toggles

Rectangle {
    color: "transparent"
    implicitHeight: Config.em(2.6)

    Row {
        id: toggles

        spacing: 5
        x: (parent.width - width) / 2

        AudioToggle {}
        BluetoothToggle {}
        WifiToggle {}
        AnimationsToggle {}
    }
}
