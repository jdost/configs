from ignis import widgets
from ignis.services.bluetooth import BluetoothDevice, BluetoothService

from bar.icon import BarIcon
from utils import toggle_class

bluetooth = BluetoothService.get_default()


class BluetoothIcon(BarIcon):
    name = "bluetooth"
    icon = "󰂯"
    priority = 5

    def render_icon(self, devices: list[BluetoothDevice], powered: bool) -> str:
        toggle_class(self.widget, "enabled", powered)
        toggle_class(self.widget, "connected", powered and bool(len(devices)))

        if not powered:
            return "󰂲"
        elif len(devices):
            return "󰂱"
        else:
            return "󰂯"

    @staticmethod
    def render_tooltip(devices: list[BluetoothDevice], powered: bool) -> str:
        if not powered:
            return "Controller: Off"
        if len(devices):
            return f"Controller: {len(devices)} device(s) connected"
        return "Controller: On"

    def setup(self, label: widgets.Label) -> None:
        self.widget = label
        self.widget.label = bluetooth.bind_many(
            ["connected_devices", "powered"], transform=self.render_icon
        )
        self.widget.tooltip_text = bluetooth.bind_many(
            ["connected_devices", "powered"], transform=self.render_tooltip
        )
