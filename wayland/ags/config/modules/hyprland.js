const hyprland = await Service.import("hyprland")
import { add_left } from "../widgets/bar.js";

const name_icons = {
    "term": "",
    "web": "爵",
    "code": "",
    "games": "",
    "chat": "ﭮ",
    "music": "ﱘ",
    "scratch": "ﴬ",
    "video": "",
};
const default_icon = "";


add_left((function Workspaces() {
    const activeId = hyprland.active.workspace.bind("id")
    const workspaces = hyprland.bind("workspaces")
        .as(workspaces => workspaces.map(function (workspace) {
            var button = Widget.Button({
                on_primary_click: () => hyprland.messageAsync(`dispatch workspace ${workspace.id}`),
                cursor: 'pointer',
                child: Widget.Label(name_icons[workspace.name] || default_icon),
                class_name: 'ws-button',
                attribute: workspace.id,
                setup: function (self) {
                    self.hook(hyprland, function () {
                        self.toggleClassName('focused', hyprland.active.workspace.id === workspace.id);
                        self.toggleClassName('occupied', hyprland.getWorkspace(workspace.id)?.windows > 0);
                    });
                },
            });
            return button;
        }))

    return Widget.Box({
        class_name: "workspaces",
        children: workspaces,
    })
})());
