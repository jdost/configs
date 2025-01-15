// Load user defined settings from JSON file
const loaded = JSON.parse(
  Utils.readFile(`${App.configDir}/settings.json`) || "{}",
);

// Default values that get overridden by JSON values
const defaults = {
  monitor: 0,
  sidebarEnabled: true,
  widgets: ["hyprland", "audio", "cpu", "memory", "systray", "clock"],
  accent: true,
  fontSize: 18,
};

export default { ...defaults, ...loaded };
