const hyprland = await Service.import("hyprland");
import { addLeft } from "../widgets/bar.js";
import { addToggle } from "../widgets/sidebar.js";

const name_icons = {
  term: "",
  web: "爵",
  code: "",
  games: "",
  chat: "ﭮ",
  music: "ﱘ",
  scratch: "ﴬ",
  video: "",
  notes: "ﴬ",
};
const default_icon = "";

addLeft(
  (function Workspaces() {
    const activeId = hyprland.active.workspace.bind("id");
    var monitorID = "";
    const workspaces = hyprland.bind("workspaces").as((workspaces) =>
      workspaces
        .toSorted(function (a, b) {
          if (a.monitorID == b.monitorID) return a.id - b.id;
          return a.monitorID - b.monitorID;
        })
        .map(function (workspace, index) {
          // Skip special workspaces
          if (workspace.id < 0) {
            return;
          }

          // Determine if moved to second monitor, inject a margin to differentiate
          const newMonitor = monitorID !== workspace.monitorID;
          monitorID = workspace.monitorID;

          var button = Widget.Button({
            on_primary_click: () =>
              hyprland.messageAsync(`dispatch workspace ${workspace.id}`),
            cursor: "pointer",
            child: Widget.Label(name_icons[workspace.name] || default_icon),
            class_names: ["ws-button", `monitor-${workspace.monitorID}`],
            // Tried `:first-child` on the monitor class, doesn't work for some reason
            css: (newMonitor && monitorID != 0) ? "margin-left: 12px" : "",
            attribute: workspace.id,
            setup: function (self) {
              self.hook(hyprland, function () {
                var visible = false;
                hyprland.monitors.forEach(function (monitor) {
                  if (monitor.activeWorkspace.id === workspace.id) {
                    self.toggleClassName("focused", monitor.focused);
                    self.toggleClassName("visible", !monitor.focused);
                    visible = true;
                  }
                });
                if (!visible) {
                  self.toggleClassName("focused", false);
                  self.toggleClassName("visible", false);
                }
                self.toggleClassName(
                  "occupied",
                  hyprland.getWorkspace(workspace.id)?.windows > 0,
                );
              });
            },
          });
          return button;
        }),
    );

    return Widget.Box({
      class_name: "workspaces",
      children: workspaces,
    });
  })(),
);

const animations_enabled = Variable(false);
function getAnimations() {
  const enabled = hyprland
    .message("getoption animations:enabled")
    .startsWith("int: 1");
  animations_enabled.value = enabled;
  return enabled;
}
addToggle({
  icon: animations_enabled.bind().as(function (en) {
    return en ? "󱥰" : "󱥱";
  }),
  tooltip: "Toggle WM Animations",
  get_state: getAnimations,
  set_state: function (s) {
    hyprland
      .messageAsync(`keyword animations:enabled ${s}`)
      .then(getAnimations);
  },
});
