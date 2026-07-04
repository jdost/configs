import Quickshell.Bluetooth
import qs.Sidebar.Toggles

ToggleBase {
    enabled: Bluetooth.defaultAdapter.enabled
    icon: enabled ? "󰂯" : "󰂲"
    onClicked: function () {
        Bluetooth.defaultAdapter.enabled = !Bluetooth.defaultAdapter.enabled;
    }
}
