import brightness from '../services/brightness.js';
import { register_hook } from "../widgets/osd.js";

const level_thresholds = [
    [0.66, "high"],
    [0.34, "medium"],
    [0.01, "low"],
    [0.0, "off"],
];

register_hook({
    name: "brightness",
    hook: [brightness, "screen-changed"],
    setup: function (box) {
        box.children = [
            Widget.Icon().hook(brightness, function (icon) {
                const level = level_thresholds.find(function ([threshold]) {
                  return threshold <= brightness.screen_value;
                })?.[1];
                icon.icon = `display-brightness-${level}-symbolic`;
            }),
            Widget.LevelBar({
                widthRequest: 200,
                max_value: 1.0,
                bar_mode: "continuous",
                value: brightness.bind("screen_value"),
            })
        ];
        return true;
    },
});
