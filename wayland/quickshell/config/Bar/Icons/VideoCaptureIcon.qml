import Quickshell.Services.Pipewire
import qs

Icon {
    property list<PwNode> devices: Pipewire.linkGroups.values.filter(g => g.source.type === PwNodeType.VideoSource).map(g => g.target)
    module: "audio"

    icon: devices.length > 0 ? "" : ""
    iconColor: U.rgba(255, 128, 0, 0.8);
    tooltip: {
        if (devices.length === 0)
            return "";
        return `Video Capture: ${devices.join()}`
    }
}
