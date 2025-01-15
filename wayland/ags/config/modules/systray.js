const systemtray = await Service.import("systemtray");
import { addRight } from "../widgets/bar.js";

function SysTrayIcon(item) {
  return Widget.Button({
    child: Widget.Icon({ icon: item.bind("icon") }),
    on_primary_click: function (_, event) {
      try {
        (item.is_menu ? item.openMenu : item.activate)(event);
      } catch (e) {
        (item.is_menu ? item.activate : item.openMenu)(event);
      }
    },
    on_secondary_click: function (_, event) {
      (item.is_menu ? item.secondaryActivate : item.openMenu)(event);
    },
    tooltip_markup: item.bind("tooltip_markup"),
  });
}

addRight(
  Widget.Box({
    children: systemtray.bind("items").as((items) => items.map(SysTrayIcon)),
    class_name: "tray",
  }),
  true,
);
