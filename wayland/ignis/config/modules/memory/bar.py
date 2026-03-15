from ignis.gobject import Binding
from ignis.utils import Poll, read_file

from bar.icon import GradientIcon


class MemoryIcon(GradientIcon):
    icon = ""
    name = "memory"
    tooltip_fmt = "RAM: {:.2%}"

    css_classes = ["big"]

    def binding(self) -> Binding:
        """
        This uses /proc/meminfo for calculating usage
        """

        def value_update(_) -> float:
            content = read_file("/proc/meminfo", decode=True)
            total, free = -1, -1
            for line in content.split("\n"):
                # The lines *should* be <METRIC_NAME>:   <VALUE>
                if ":" not in line:
                    continue
                k, v = line.split(":")
                if k.strip() == "MemTotal":
                    total = int(v.strip().split(" ")[0])
                elif k.strip() == "MemFree":
                    free = int(v.strip().split(" ")[0])

            # If we didn't find total or free, default to 0
            if total == -1 or free == -1:
                return 0.0

            return (total - free) / total

        return Poll(1000, callback=value_update).bind("output")
