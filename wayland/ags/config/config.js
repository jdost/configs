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

App.resetCss();
Utils.monitorFile(`${App.configDir}/style.css`, function () {
  App.resetCss();
  App.applyCss(`${App.configDir}/style.css`);
});

App.config({
  style: "./style.css",
  iconTheme: "Papirus",
  windows:
    [
      bar(settings.monitor),
      osd(settings.monitor),
      notifications(settings.monitor),
    ] + (settings.accent ? [accent(settings.monitor)] : []),
});
