import Quickshell.Services.UPower
import qs

Icon {
    readonly property list<string> batteryIcons: [..."󰂎󰁺󰁻󰁼󰁽󰁾󰁿󰂀󰂁󰂂󰁹"]
    readonly property string chargedIcon: ""
    property bool isCharging: !UPower.onBattery
    property var battery: UPower.displayDevice
    property real batteryLevel: battery.percentage
    property bool isFull: battery.state === UPowerDeviceState.FullyCharged

    function readableTime(totalSecs: real): string {
        var output = "";
        const hours = Math.floor(totalSecs / (60 * 60));
        const minutes = Math.floor((totalSecs / 60) % 60);

        if (hours)
            output += `${hours}h`;
        if (minutes)
            output += `${minutes}m`;
        // Trick, XhXXmXXs is long, so truncate to XhXXm, but XhXXs and XXmXXs are fine
        if (minutes && hours)
            return output

        output += `${totalSecs % 60}s`;
        return output;
    }

    icon: {
        if (isFull && isCharging)
            return chargedIcon;

        return batteryIcons[Math.round((batteryIcons.length - 1)*batteryLevel)];
    }
    iconColor: {
        if (isFull || isCharging)
            return U.rgba(255, 255, 255, 1.0);
        // Gradient for battery is backwards, high is good, low is bad
        return U.gradientColor(1-batteryLevel);
    }
    module: "battery"
    size: Config.em(1.0)
    tooltip: {
        if (isFull)
            return "Charged";
        if (battery.timeToEmpty)
            return `Discharging: ${readableTime(battery.timeToEmpty)} remaining`;
        if (battery.timeToFull)
            return `Charging: ${readableTime(battery.timeToFull)} until full`;
        return "Unknown";
    }
    topPadding: -Config.em(0.1)
}
