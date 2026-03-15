from typing import ClassVar, Optional, Sequence

from ignis import widgets
from ignis.gobject import Binding

from bar.widget import BarSide, BarWidget
from utils import color


class BarIcon(BarWidget):
    label: str = ""
    base = widgets.Label
    __build_props__ = {"label", *BarWidget.__build_props__}

    def __init__(self, *args, **kwargs) -> None:
        if hasattr(self, "icon"):
            self.label = self.icon

        if not hasattr(self, "css_classes"):
            self.css_classes = []

        self.css_classes.append(self.name)
        self.css_classes.append("icon")
        super().__init__(*args, **kwargs)

    @classmethod
    def register(cls) -> None:
        BarIconsWidget.register_icon(cls)


class GradientIcon(BarIcon):
    gradient: Sequence[color.Color] = [color.GREEN, color.YELLOW, color.RED]
    tooltip_fmt: Optional[str] = None

    def __init__(self, *args, **kwargs) -> None:
        if not hasattr(self, "css_classes"):
            self.css_classes = []

        self.css_classes.append("gradient")
        super().__init__(*args, **kwargs)

    def binding(self) -> Binding:
        raise NotImplementedError

    def _calculate_color(self, value) -> color.Color:
        if value > 1.1:
            # TODO use logging
            print(
                f"ERROR: gradient calculate value out of bounds: {value}, expected between 0.0 and 1.0"
            )
            return color.GREY

        # If at a perfect interval (0, 0.5, or 1.0), just give the number
        level = value * (len(self.gradient) - 1)
        if level % 1 == 0:
            return self.gradient[int(level)]

        # TODO guard against out-of-bounds variable ranges
        floor = self.gradient[int(level // 1)]
        ceiling = self.gradient[int(level // 1) + 1]

        return color.Color(
            round(floor.red + (ceiling.red - floor.red) * (level % 1)),
            round(floor.green + (ceiling.green - floor.green) * (level % 1)),
            round(floor.blue + (ceiling.blue - floor.blue) * (level % 1)),
        )

    def _calculate_style(self, value) -> str:
        return f"color: {self._calculate_color(value).as_rgb()};"

    def setup(self, widget) -> None:
        binding = self.binding()
        binding._transform = self._calculate_style

        widget.style = binding
        if not self.tooltip_fmt:
            return

        widget.tooltip_text = Binding(
            target=binding.target,
            target_properties=binding.target_properties,
            transform=lambda x: self.tooltip_fmt.format(x),
        )


class BarIconsWidget(BarWidget):
    _icons: ClassVar[list[type[BarIcon]]] = []
    side = BarSide.RIGHT
    priority = 0

    base = widgets.Box
    css_classes = ["icons"]
    spacing = 6

    @classmethod
    def register_icon(cls, icon: type[BarIcon]) -> None:
        cls._icons.append(icon)

    def setup(self, widget) -> None:
        widget.child = [
            icon.build(self.monitor_id)
            for icon in sorted(self._icons, key=BarIcon.sort_key)
        ]
