from ignis.gobject import Binding
from ignis.utils import Poll, read_file

from bar.icon import GradientIcon


class CpuIcon(GradientIcon):
    icon = ""
    name = "cpu"
    tooltip_fmt = "CPU: {:.2%}"

    css_classes = ["big"]

    def binding(self) -> Binding:
        """
        This uses /proc/stat for tracking usage, which requires historical context
        to measure usage across intervals.  The `last` tuple stores the previously
        calculated usage and total counts of cpu time.

        On each poll update, we parse out the different categories of CPU usage
        and sum them to get usage and total cpu time, then remove the values
        previously calculate (otherwise we get full historical usage and not
        recent windows).  We track the previous sums to calculate the interval
        amount using `last`.
        """
        last = (-1, -1)

        def value_update(_) -> float:
            nonlocal last

            output = 0.0
            content = read_file("/proc/stat", decode=True)
            # This looks like:
            # `cpu  2255 34 2290 22625563 6290 127 456`
            # We drop the label, irq, and softirq
            _, user, nice, system, idle, iowait, _, _, steal = content.split("\n")[
                0
            ].split()[:9]
            usage = int(user) + int(nice) + int(system) + int(iowait) + int(steal)
            total = usage + int(idle)

            # if this is the first iteration, we don't show the historical amount
            if last[0] != -1:
                output = (usage - last[0]) / (total - last[1])

            last = (usage, total)
            return output

        return Poll(1000, callback=value_update).bind("output")
