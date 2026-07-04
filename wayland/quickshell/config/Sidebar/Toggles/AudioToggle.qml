import Quickshell.Services.Pipewire
import qs.Sidebar.Toggles

ToggleBase {
    property PwNode device: Pipewire.defaultAudioSource
    enabled: (device && device.audio) ? device.audio.muted : false
    icon: enabled ? "󰍭" : "󰍬"
    onClicked: function () {
        device.audio.muted = !device.audio.muted;
    }
}
