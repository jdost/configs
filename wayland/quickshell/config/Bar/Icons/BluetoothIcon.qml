import Quickshell.Bluetooth
import qs
import qs.Popups

Icon {
    property bool isEnabled: (Bluetooth.defaultAdapter && Bluetooth.defaultAdapter.enabled)
    property bool isConnected: Bluetooth.devices.values.filter((d) => {
        return d.connected;
    }).length > 0

    icon: {
        if (!isEnabled)
            return "󰂲";

        if (isConnected)
            return "󰂱";

        return "󰂯";
    }
    iconColor: {
        if (!isEnabled)
            return U.rgba(153, 153, 153, 1);

        if (isConnected)
            return U.rgba(85, 170, 255, 1);

        return U.rgba(255, 255, 255, 1);
    }
    module: "bluetooth"
    size: {
        if (isConnected)
            return Config.em(1.3);

        return Config.em(1);
    }
    tooltip: {
        if (!isEnabled)
            return "Controller: Off";

        if (isConnected)
            return `Connected: ${Bluetooth.devices.values.filter((d) => d.connected).length} device(s)`;

        return "Controller: On";
    }
    topPadding: {
        if (isConnected)
            return -Config.em(0.1);

        return -Config.em(0.15);
    }
    onClicked: function() {
        popup.toggle();
    }

    BluetoothPopup {
        id: popup

        timeout: 15000
    }

}
