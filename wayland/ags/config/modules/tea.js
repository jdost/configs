import { calcGradientColor } from "../widgets/icons.js";
import { add_icon } from "../widgets/bar.js";

const TIMER_LENGTH = 200;
const INTERVAL_PERIOD = 5;
const DEFAULT_COLOR = "rgb(190, 190, 190)";
const GRADIENT = [
  [255, 255, 255],
  [155, 80, 0],
];
const icon = Widget.Label({
  label: "󰶞",
  css: `color: ${DEFAULT_COLOR}`,
  tooltip_text: `TeaTimer: ${TIMER_LENGTH}s`,
});

add_icon(
  Widget.EventBox({
    class_name: "tea",
    cursor: "pointer",
    child: icon,
    on_primary_click: function (_) {
      let remaining = TIMER_LENGTH;
      icon.tooltip_text = "TeaTimer Running";
      icon.css = `color: ${calcGradientColor(GRADIENT, 0.0)}`;

      const timer = setInterval(function () {
        remaining -= INTERVAL_PERIOD;
        if (remaining <= 0) {
          icon.tooltip_text = "TeaTimer Finished";
          const nag = Widget.Window({
            name: "ags.popup.teatimer",
            class_name: "teatimer nag",
            child: Widget.Box({
              vertical: true,
              children: [
                Widget.Label("󰶞"),
                Widget.Button({
                  cursor: "pointer",
                  child: Widget.Label("Clear"),
                  onClicked: function (_) {
                    icon.tooltip_text = `TeaTimer: ${TIMER_LENGTH}s`;
                    nag.close();
                    icon.css = `color: ${DEFAULT_COLOR}`;
                  },
                }),
              ],
            }),
          });
          timer.destroy();
        } else {
          icon.css = `color: ${calcGradientColor(
            GRADIENT,
            (TIMER_LENGTH - remaining) / TIMER_LENGTH,
          )}`;
        }
      }, INTERVAL_PERIOD * 1000);
    },
  }),
  -1,
);
