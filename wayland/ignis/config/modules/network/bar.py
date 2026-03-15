from ignis import widgets
from ignis.services.network import NetworkService, WifiDevice
from ignis.utils import Poll

from bar.icon import BarIcon
from utils.widgets import BaseWidget

network = NetworkService.get_default()

ETHERNET_ICON = ""
AIRPLANE_ICON = "󰀝"
WIFI_STRENGTH_ICONS = "󰤟󰤢󰤥󰤨"
WIFI_DISCONNECTED_ICON = "󰤮"
VPN_ICON = "󰳌"


class NetworkIcon(BarIcon):
    name = "network"
    priority = 5
    base = widgets.Overlay
    __build_props__ = BaseWidget.__build_props__
    css_classes = ["icon", "network"]

    def __init__(self, monitor_id: int) -> None:
        self._wifi_device: WifiDevice | None = None
        super().__init__(monitor_id)

    def track_wifi(self, added: bool) -> None:
        if not added:
            return

        for device in network.wifi.devices:
            if not device.is_connected:
                continue

            self._wifi_device = device

    def update(self, *_) -> None:
        if network.ethernet.is_connected:
            self.network_icon.label = ETHERNET_ICON
            self.overlay.tooltip_text = "Ethernet - connected"
        elif network.wifi.is_connected:
            strength = self._wifi_device.ap.strength if self._wifi_device else 50
            self.network_icon.label = WIFI_STRENGTH_ICONS[
                min(
                    round(strength / 100 * (len(WIFI_STRENGTH_ICONS) - 1)),
                    len(WIFI_STRENGTH_ICONS) - 1,
                )
            ]
            if self._wifi_device:
                self.overlay.tooltip_text = (
                    f"Wifi - {self._wifi_device.ap.ssid} ({strength}%)"
                )
            else:
                self.overlay.tooltip_text = "Wifi - connected"
        elif not network.wifi.enabled:
            self.network_icon.label = AIRPLANE_ICON
            self.overlay.tooltip_text = ""
        else:
            self.network_icon.label = WIFI_DISCONNECTED_ICON
            self.overlay.tooltip_text = ""

        if network.vpn.is_connected:
            self.vpn_icon.label = VPN_ICON
            self.overlay.tooltip_text = f"(VPN) {self.overlay.tooltip_text}"
        else:
            self.vpn_icon.label = ""

    def render_child(self) -> widgets.Label:
        self.network_icon = widgets.Label(css_classes=["icon"])
        return self.network_icon

    def setup(self, overlay: widgets.Overlay) -> None:
        self.overlay = overlay

        self.vpn_icon = widgets.Label(
            css_classes=["badge"],
        )
        self.overlay.overlays = [self.vpn_icon]

        network.ethernet.bind("is_connected", transform=self.update)
        network.wifi.bind_many(["is_connected", "enabled"], transform=self.update)
        network.wifi.bind("is_connected", transform=self.track_wifi)

        if network.wifi.is_connected:
            self.track_wifi(True)

        Poll(10000, self.update)
