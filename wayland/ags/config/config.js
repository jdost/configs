import bar from "./widgets/bar.js";
import notifications from "./widgets/notifications.js";
import osd from "./widgets/osd.js";
import "./modules/hyprland.js";
import "./modules/audio.js";
import "./modules/bluetooth.js";
import "./modules/battery.js";
import "./modules/network.js";
import "./modules/cpu.js";
import "./modules/memory.js";
import "./modules/systray.js";
import "./modules/clock.js";

const accent = Widget.Window({
  name: "ags.accent",
  class_name: "accent",
  exclusivity: "ignore",
  anchor: ["top", "left", "right"],
  child: Widget.CenterBox({
    center_widget: Widget.Box({
      children: [],
    }),
  }),
});

App.resetCss();
Utils.monitorFile(`${App.configDir}/style.css`, function () {
  App.resetCss();
  App.applyCss(`${App.configDir}/style.css`);
});

App.config({
  style: "./style.css",
  iconTheme: "Papirus",
  windows: [accent, bar(0), osd(0), notifications()],
});
