from ignis import widgets
from ignis.services.upower import UPowerService

from bar.icon import BarIcon
from utils import color

upower = UPowerService.get_default()
CHARGE_ICONS = "󰂎󰁺󰁻󰁼󰁽󰁾󰁿󰂀󰂁󰂂󰁹"


class BatteryIcon(BarIcon):
    name = "battery"
    priority = 10

    _STATUS_PROPS = ["percent", "charging", "charged"]

    @staticmethod
    def resolve_icon(percent: float, charging: bool, charged: bool) -> str:
        if charged:
            return ""

        return CHARGE_ICONS[
            min(
                int((percent / 100) * len(CHARGE_ICONS) // 1),
                len(CHARGE_ICONS) - 1,
            )
        ]

    @staticmethod
    def resolve_color(percent: float, charging: bool, charged: bool) -> str:
        if charged or charging:
            return f"color: {color.WHITE.as_rgb()};"

        if percent > 50.0:
            return (
                f"color: mix({color.YELLOW.as_rgb()}, "
                f"{color.GREEN.as_rgb()}, {(percent - 50) / 50});"
            )
        else:
            return (
                f"color: mix({color.RED.as_rgb()}, "
                f"{color.YELLOW.as_rgb()}, {percent / 50});"
            )

    @staticmethod
    def resolve_status(time_remaining: int, charging: bool, charged: bool) -> str:
        if charged:
            return "Charged"

        hours = time_remaining // (60 * 60)
        minutes = (time_remaining // 60) % 60
        if hours:
            time_str = f"{hours}h{minutes}m"
        else:
            time_str = f"{minutes}m"

        if charging:
            return f"Charging: {time_str} until full"
        else:
            return f"Discharging: {time_str} remaining"

    def setup(self, widget: widgets.Label) -> None:
        widget.label = upower.batteries[0].bind_many(
            self._STATUS_PROPS, self.resolve_icon
        )
        widget.style = upower.batteries[0].bind_many(
            self._STATUS_PROPS, self.resolve_color
        )
        widget.tooltip_text = upower.batteries[0].bind_many(
            ["time_remaining", "charging", "charged"], self.resolve_status
        )
