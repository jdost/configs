import QtQuick
import qs
import qs.Services

Icon {
    readonly property list<string> wifiIcons: [..."󰤟󰤢󰤥󰤨"];

    module: "network"
    icon: {
        if (NetworkService.airplaneMode)
            return "󰀝";
        if (!NetworkService.isConnected)
            return "󰤮";
        if (!NetworkService.isWifi)
            return "";
        return wifiIcons[Math.round((wifiIcons.length - 1)*NetworkService.wifiStrength)];
    }
    size: Config.em(1.5)
    iconColor: U.rgb(255, 255, 255)
    tooltip: {
        if (!NetworkService.isWifi)
            return "";
        return `Connected: ${NetworkService.wifiSSID}`;
    }

    // This is a smaller icon in the bottom right that is used to give more overlayed information
    // on connectivity, things like VPN being connected or the connectivity check results being limited
    Text {
        id: badge
        antialiasing: false
        text: {
            return ""
        }
        color: U.rgb(255, 255, 255)
        x: Config.em(0.4)
        y: Config.em(0.3)
        font.pixelSize: Config.em(0.7)
    }
}
