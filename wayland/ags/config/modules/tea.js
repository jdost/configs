import { calcGradientColor } from "../widgets/icons.js";
import { add_icon } from "../widgets/bar.js";
import { Popup } from "../widgets/popup.js";

const target = Variable(200);
const active = Variable(0);
const TARGET_MAX = 600;
const TARGET_MIN = 30;
const INTERVAL_PERIOD = 5;
const DEFAULT_COLOR = "rgb(190, 190, 190)";
const GRADIENT = [
  [255, 255, 255],
  [255, 160, 40],
];
const icon = Widget.Label({
  label: "󰶞",
  css: `color: ${DEFAULT_COLOR}`,
  tooltip_text: Utils.merge([target.bind(), active.bind()], function (t, a) {
    if (a < 0) return "TeaTimer Finished";
    else if (a > 0) return "TeaTimer Running";

    return `TeaTimer: ${timeToString(t)}`;
  }),
});

function timeToString(time_sec) {
  const min = Math.floor(time_sec / 60);
  const sec = Math.floor(time_sec % 60);
  if (sec < 10) return `${min}:0${sec}`;
  return `${min}:${sec}`;
}

const popup = Popup({
  name: "teatimer",
  timeout: 3000,
  setup: function (window) {
    const slider = Widget.Slider({
      hexpand: true,
      drawValue: false,

      min: TARGET_MIN,
      value: target.bind(),
      max: TARGET_MAX,

      onChange: function (s) {
        target.value = s.value;
        popup.refresh();
      },
    });
    const labels = Widget.Box({
      halign: "center",
      children: [
        Widget.Label({
          hexpand: true,
          label: target.bind().as(function (v) {
            return `Duration: ${timeToString(v)}`;
          }),
        }),
      ],
    });
    window.child = Widget.Box({
      vertical: true,
      children: [labels, slider],
    });
  },
});

add_icon(
  Widget.EventBox({
    class_name: "teatimer",
    cursor: "pointer",
    child: icon,
    on_primary_click: function (_) {
      let remaining = Math.floor(target.value);
      icon.css = `color: ${calcGradientColor(GRADIENT, 0.0)}`;
      active.value = 1;
      popup.close();

      const timer = setInterval(function () {
        remaining -= INTERVAL_PERIOD;
        if (remaining <= 0) {
          active.value = -1;
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
                    nag.close();
                    active.value = 0;
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
            (target.value - remaining) / target.value,
          )}`;
        }
      }, INTERVAL_PERIOD * 1000);
    },
    on_secondary_click: function (_) {
      if (!active.value > 0) popup.toggle();
    },
  }),
  -1,
);
