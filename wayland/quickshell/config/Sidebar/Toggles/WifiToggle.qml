import Quickshell.Networking as NM
import qs
import qs.Services
import qs.Sidebar.Toggles

ToggleBase {
    enabled: !NetworkService.airplaneMode
    icon: enabled ? "󰖩" : "󰖪"
    onClicked: function () {
        NM.Networking.wifiEnabled = !NM.Networking.wifiEnabled;
    }
    visible: Config.enabled("network")
}
