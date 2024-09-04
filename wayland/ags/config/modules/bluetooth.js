const bluetooth = await Service.import("bluetooth");
import { add_icon } from "../widgets/bar.js";

let popup = null;

function popup_close() {
  if (popup === null) {
    return;
  }
  popup.close();
  popup = null;
}

add_icon(
  Widget.EventBox({
    class_name: "bluetooth",
    on_primary_click: function (_, e) {
      if (popup !== null) {
        return popup_close();
      }

      var popupButtons = bluetooth.devices.map(function (dev) {
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
      popupButtons.splice(
        0,
        0,
        Widget.ToggleButton({
          cursor: "pointer",
          child: Widget.Box({
            vertical: true,
            children: [
              Widget.Icon({ icon: "bluetooth", size: 48 }),
              Widget.Label({ label: "Controller" }),
            ],
          }),
          onToggled: function (_) {
            bluetooth.toggle();
            popup_close();
          },
          active: bluetooth.enabled,
        }),
      );

      popup = Widget.Window({
        class_name: "bluetooth-connections",
        name: "ags.popup.bluetooth",
        anchor: ["top", "right"],
        child: Widget.Box({
          spacing: 2,
          children: popupButtons,
        }),
      });
      return popup;
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
            } else if (devices.length > 0) {
              self.label = "󰂱";
            } else {
              self.label = "󰂯";
            }
          },
        );
      },
    }),
  }),
  5,
);
