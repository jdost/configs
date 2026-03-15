from ignis.css_manager import CssInfoPath, CssManager

css_manager = CssManager.get_default()

from utils import config_root


def add_style(module_name: str) -> None:
    css_manager.apply_css(
        CssInfoPath(
            name=module_name,
            path=str(config_root() / module_name.replace(".", "/") / "style.css"),
        )
    )
