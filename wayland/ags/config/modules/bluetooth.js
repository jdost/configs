const bluetooth = await Service.import("bluetooth");
import { add_icon } from "../widgets/bar.js";
import { Popup } from "../widgets/popup.js";
import { addToggle } from "../widgets/sidebar.js";

const popup = Popup({
  name: "bluetooth",
  timeout: 5000,
  setup: function (window) {
    window.class_names.push("bluetooth-connections");

    var popupButtons = bluetooth.devices.map(function (dev) {
      if (!dev.paired) return;
      return Widget.Button({
        class_name: dev.connected ? "connected" : "",
        cursor: "pointer",
        on_clicked: function (x, y) {
          dev.setConnection(!dev.connected);
          popup_close();
        },
        child: Widget.Box({
          vertical: true,
          children: [
            Widget.Icon({ icon: dev["icon-name"], size: 48 }),
            Widget.Label({ label: dev.alias }),
          ],
        }),
      });
    });

    window.child = Widget.Box({
      spacing: 2,
      homogeneous: true,
      children: popupButtons,
    });

    return;
  },
});

addToggle({
  icon: bluetooth.bind("enabled").as(function (en) {
    return en ? "󰂯" : "󰂲";
  }),
  tooltip: bluetooth.bind("enabled").as(function (en) {
    return en ? "Turn off Bluetooth" : "Turn on Bluetooth";
  }),
  get_state: function () {
    return bluetooth.enabled;
  },
  set_state: function (s) {
    if (s && !bluetooth.enabled) bluetooth.toggle();
    else if (!s && bluetooth.enabled) bluetooth.toggle();
  },
});

add_icon(
  Widget.EventBox({
    class_name: "bluetooth",
    on_primary_click: function (_, e) {
      return popup.toggle();
    },
    child: Widget.Label({
      setup: function (self) {
        Utils.merge(
          [bluetooth.bind("connected-devices"), bluetooth.bind("enabled")],
          function (devices, enabled) {
            self.toggleClassName("enabled", enabled);
            self.toggleClassName("connected", devices.length > 0);

            if (!enabled) {
              self.label = "󰂲";
              self.tooltip_text = "Controller: Off";
            } else if (devices.length > 0) {
              self.label = "󰂱";
              self.tooltip_text = `Connected: {devices.length} device(s)`;
            } else {
              self.label = "󰂯";
              self.tooltip_text = "Controller: On";
            }
          },
        );
      },
    }),
  }),
  5,
);
