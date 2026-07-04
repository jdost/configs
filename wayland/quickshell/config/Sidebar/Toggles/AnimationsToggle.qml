import qs
import qs.Sidebar.Toggles

ToggleBase {
    enabled: Config.animations
    icon: enabled ? "󱥰" : "󱥱"
    onClicked: function () {
        // TODO: figure out hyprctl toggling w/ lua, toggle command:
        // `hyprctl eval 'hl.config({animations={enabled=not hl.get_config("animations.enabled")}})'`
        Config.animations = !Config.animations;
    }
}
