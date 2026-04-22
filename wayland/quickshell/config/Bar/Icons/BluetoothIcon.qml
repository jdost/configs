import Quickshell.Bluetooth
import qs

Icon {
    property bool isEnabled: (Bluetooth.defaultAdapter && Bluetooth.defaultAdapter.enabled)
    property bool isConnected: Bluetooth.devices.values.filter((d) => d.connected).length > 0

    icon: {
        if (!isEnabled)
            return "󰂲";
        if (isConnected)
            return "󰂱";
        return "󰂯";
    }
    iconColor: {
        if (!isEnabled)
            return U.rgba(153, 153, 153, 1.0);
        if (isConnected)
            return U.rgba(85, 170, 255, 1.0);
        return U.rgba(255, 255, 255, 1.0);
    }
    module: "bluetooth"
    size: {
        if (isConnected)
            return Config.em(1.3)
        return Config.em(1.0)
    }
    tooltip: {
        if (!isEnabled)
            return "Controller: Off"
        if (isConnected)
            return `Connected: ${Bluetooth.devices.values.filter((d) => d.connected).length} device(s)`
        return "Controller: On"
    }
    topPadding: {
        if (isConnected)
            return -3;
        return -4;
    }
}
