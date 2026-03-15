from ignis import widgets
from ignis.gobject import Binding
from ignis.services.hyprland import HyprlandService, HyprlandWorkspace

from bar.widget import BarMonitor, BarSide, BarWidget
from utils import cursor
from utils.widgets import BaseWidget

hyprland = HyprlandService.get_default()

ICONS = {
    "term": "",
    "web": "爵",
    "code": "",
    "games": "",
    "chat": "ﭮ",
    "music": "ﱘ",
    "scratch": "ﴬ",
    "video": "",
    "notes": "ﴬ",
}
DEFAULT_ICON = ""


class WorkspaceButton(BaseWidget):
    base = widgets.Button

    def __init__(self, workspace: HyprlandWorkspace, is_active: bool) -> None:
        self.css_classes = ["ws-button"]
        self.workspace = workspace
        is_focused = False

        if is_active:
            is_focused = self.is_focused
            self.css_classes.append("focused" if is_focused else "visible")

        if hyprland.get_windows_on_workspace(workspace.id):
            self.css_classes.append("occupied")

        self.cursor = cursor("arrow") if is_focused else cursor("pointer")

    @property
    def is_focused(self) -> bool:
        return hyprland.get_monitor_by_name(self.workspace.monitor).focused

    def on_click(self, *_) -> None:
        self.workspace.switch_to()

    def render_child(self) -> widgets.Label:
        return widgets.Label(label=ICONS.get(self.workspace.name, DEFAULT_ICON))


class WorkspacesWidget(BarWidget):
    name = "workspaces"
    side = BarSide.LEFT
    monitor = BarMonitor.ALL

    base = widgets.Box
    css_classes = ["workspaces"]

    def render_buttons(
        self,
        workspaces: list[HyprlandWorkspace],
        active_workspace: HyprlandWorkspace,
    ) -> list[widgets.Button]:
        return [
            WorkspaceButton(workspace, workspace.id == active_workspace.id).render()
            for workspace in workspaces
            if (workspace.monitor_id == self.monitor_id and workspace.id >= 0)
        ]

    def render_children(self) -> Binding:
        return hyprland.bind_many(
            ["workspaces", "active_workspace"],
            transform=self.render_buttons,
        )
