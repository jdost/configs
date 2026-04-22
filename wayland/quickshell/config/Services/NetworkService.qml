pragma Singleton

import Quickshell
import Quickshell.Networking as NM

Singleton {
    id: networkService

    property bool airplaneMode: (!NM.Networking.wifiHardwareEnabled || !NM.Networking.wifiEnabled);
    property bool isConnected: {
        NM.Networking.devices.values.some((d) => d.connected);
    }
    property var connectedDevice: {
        return NM.Networking.devices.values.find((d) => d.connected);
    }
    property bool isWifi: {
        if (connectedDevice === undefined)
            return false;
        return connectedDevice.type === NM.DeviceType.Wifi
    }
    property var wifiNetwork: {
        if (!isWifi)
            return undefined;
        return connectedDevice.networks.values.find((n) => n.connected);
    }
    property string wifiSSID: wifiNetwork ? wifiNetwork.name : "";
    property real wifiStrength: wifiNetwork ? wifiNetwork.signalStrength : 0.0;
}
