const hyprland = await Service.import("hyprland");
import { add_left } from "../widgets/bar.js";

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

add_left(
  (function Workspaces() {
    const activeId = hyprland.active.workspace.bind("id");
    var monitorID = "";
    const workspaces = hyprland.bind("workspaces").as((workspaces) =>
      workspaces.map(function (workspace, index) {
        const newMonitor =
          index > 0 ? monitorID !== workspace.monitorID : false;
        monitorID = workspace.monitorID;
        if (workspace.id < 0) {
          return;
        }
        var button = Widget.Button({
          on_primary_click: () =>
            hyprland.messageAsync(`dispatch workspace ${workspace.id}`),
          cursor: "pointer",
          child: Widget.Label(name_icons[workspace.name] || default_icon),
          class_names: ["ws-button", `monitor-${workspace.monitorID}`],
          css: newMonitor ? "margin-left: 12px" : "",
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
