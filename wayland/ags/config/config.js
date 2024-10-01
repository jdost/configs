// Setting loading, defaults w/ configured overrides
import defaultSettings from "./defaultSettings.js";
const loadedSettings = JSON.parse(
  Utils.readFile(`${App.configDir}/settings.json`) || "{}",
);
const settings = { ...defaultSettings, ...loadedSettings };

import accent from "./widgets/accent.js";
import bar from "./widgets/bar.js";
import notifications from "./widgets/notifications.js";
import osd from "./widgets/osd.js";

// Dynamically load the modules based on config
for (const module of settings.widgets) {
  await import(`./modules/${module}.js`);
}

function apply_font_size() {
  App.applyCss(`
  window {
    font-size: ${settings.fontSize}px;
  }`)
}
App.resetCss();
apply_font_size()
Utils.monitorFile(`${App.configDir}/style.css`, function () {
  App.resetCss();
  apply_font_size();
  App.applyCss(`${App.configDir}/style.css`);
});

App.config({
  style: "./style.css",
  iconTheme: "Papirus",
  windows:
    (settings.accent ? [accent(settings.monitor)] : []) + [
      bar(settings.monitor),
      osd(settings.monitor),
      notifications(settings.monitor),
    ],
});
