from importlib import import_module
from pathlib import Path

import ignis.css_manager as css
import settings
from accent import Accent
from bar import Bar
from gi.repository import Gtk  # type: ignore
from notifications import Notifications
from osd import OSD
from popup import Popup

Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
Gtk.Settings.get_default().set_property("gtk-icon-theme-name", "Papirus-Dark")
Gtk.Settings.get_default().set_property("gtk-theme-name", "Adwaita")


def css_setup() -> None:
    css_manager = css.CssManager.get_default()
    css_manager.reset_css()
    css_manager.apply_css(
        css.CssInfoPath(name="main", path=Path(__file__).parent / "style.css")
    )
    css_manager.apply_css(
        css.CssInfoString(
            name="font-adjustment",
            string=f"window {{font-size: {settings.font_size}px; }}",
        )
    )

    def trigger_all_reload(target: css.CssInfoBase) -> None:
        if target.name != "main":
            return

        for css_info in css_manager.list_css_info_names():
            if css_info == "main":
                continue
            css_manager.reload_css(css_info)

    css_manager.connect("css_reloaded", lambda _, tgt: trigger_all_reload(tgt))


def main() -> None:
    css_setup()
    for module in settings.modules:
        import_module(f"modules.{module}").setup()

    Accent.init()
    Bar.init()
    Notifications.init()
    OSD.init()
    Popup.init()


main()
