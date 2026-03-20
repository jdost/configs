from ignis import utils, widgets
from utils.style import add_style

from .hook import OSDHook


class OSD:
    def __init__(self, monitor_id: int) -> None:
        self.window = widgets.Window(
            namespace=f"ignis.osd.{monitor_id}",
            css_classes=["osd"],
            monitor=monitor_id,
            exclusivity="ignore",
            anchor=["bottom"],
            visible=False,
        )

        self.timeout = None
        self.hooks: list[OSDHook] = []
        self.active_hook: None | OSDHook = None
        utils.Timeout(ms=500, target=self.setup)

    def setup(self) -> None:
        for hook_builder in OSDHook._registry:
            hook = hook_builder()
            hook.connect("display", self.display_hook)
            self.hooks.append(hook)

    def display_hook(self, hook: OSDHook) -> None:
        if self.active_hook and self.active_hook is not hook:
            # If there is another active hook being displayed, replace it
            self.window.child.unrealize()
            self.active_hook = hook

        # If there is a visibility timer, reset it
        if self.window.visible and self.timeout:
            self.timeout.cancel()
        # If the hook isn't currently rendered, render it
        elif not self.window.visible:
            self.window.child = hook.render()
            self.window.visible = True

        self.timeout = utils.Timeout(ms=hook.timeout, target=self.close)

    def close(self) -> None:
        self.active_hook = None
        self.timeout = None
        self.window.child.unrealize()
        self.window.visible = False

    @classmethod
    def init(cls) -> None:
        add_style(__name__)
        cls(0)
