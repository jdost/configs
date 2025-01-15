const battery = await Service.import("battery");
import { addIcon } from "../widgets/bar.js";

const verticalBatteryIcons = [..."󰂎󰁺󰁻󰁼󰁽󰁾󰁿󰂀󰂁󰂂󰁹"];
const horizontalBatteryIcons = [...""];
const batteryLevelIcons = verticalBatteryIcons;

addIcon(
  Widget.Label({
    class_name: "battery",
    attribute: battery.bind("percent"),
    tooltip_text: battery.bind("time-remaining").as(function (time_sec) {
      var time_str = "";
      const hours = Math.floor(time_sec / (60 * 60));
      const mins = Math.floor(time_sec / 60) % 60;

      if (hours > 0) time_str += `${hours}h`;
      if (mins > 0) time_str += `${mins}m`;
      time_str += `${time_sec % 60}s`;

      if (battery.charging) return `Charging ${time_str} until full`;

      return `Discharging, ${time_str} remaining`;
    }),
    setup: function (self) {
      Utils.merge(
        [
          battery.bind("percent"),
          battery.bind("charging"),
          battery.bind("charged"),
        ],
        function (level, direction, isFull) {
          var color = "#FFFFFF";
          if (!direction) {
            if (level < 50)
              color = `mix(rgb(255, 0, 0), rgb(255, 255, 0), ${level / 50})`;
            else
              color = `mix(rgb(255, 255, 0), rgb(0, 255, 0), ${(level - 50) / 50})`;
          }

          self.css = `color: ${color};`;
          if (isFull) {
            self.label = "";
            return;
          }
          if (level < 0) {
            level = 100;
          }

          self.label =
            batteryLevelIcons[
              Math.floor((level / 101) * batteryLevelIcons.length)
            ];
        },
      );
    },
  }),
  10,
);
