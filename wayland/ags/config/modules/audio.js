const audio = await Service.import("audio");
import { LevelDots } from "../widgets/icons.js";
import { add_icon } from "../widgets/bar.js";
import { register_hook } from "../widgets/osd.js";

// these are lower threshold and value, threshold max is 1 less than next level
const level_thresholds = [
  [67, "high"],
  [34, "medium"],
  [1, "low"],
  [0, "muted"],
];
function volume_to_icon_level(volume) {
  const adjusted_volume = volume * 100;
  return level_thresholds.find(function ([threshold]) {
    return threshold <= adjusted_volume;
  })?.[1];
}

add_icon(
  Widget.EventBox({
    child: Widget.Box({
      class_name: "audio",
      spacing: 0,
      children: [LevelDots(audio.speaker), LevelDots(audio.microphone)],
    }),
    on_secondary_click: function (_, e) {
      let sources = Widget.MenuItem({
        child: Widget.Label("sources"),
      });
      sources.set_submenu(
        Widget.Menu({
          children: [
            Widget.MenuItem({ child: Widget.Label("A") }),
            Widget.MenuItem({ child: Widget.Label("B") }),
            Widget.MenuItem({ child: Widget.Label("C") }),
          ],
        }),
      );
      let menu = Widget.Menu({
        children: [sources],
      });
      menu.popup_at_pointer(e);
    },
  }),
  10,
);

// Last check state to catch false updates
var last_state = [false, 0];
Utils.timeout(250, function () {
  last_state = [audio.speaker.isMuted || false, audio.speaker.volume];
});

register_hook({
  name: "audio-volume",
  hook: [audio, "speaker-changed"],
  setup: function (box) {
    var current_state = [audio.speaker.isMuted, audio.speaker.volume];
    if (
      current_state[0] === last_state[0] &&
      current_state[1] === last_state[1]
    ) {
      return false;
    }

    last_state = current_state;
    box.children = [
      Widget.Icon().hook(audio.speaker, function (icon) {
        const volume = audio.speaker.isMuted ? 0 : audio.speaker.volume;
        icon.icon = `audio-volume-${volume_to_icon_level(volume)}`;
      }),
      Widget.LevelBar({
        widthRequest: 200,
        max_value: 1.5,
        bar_mode: "continuous",
        value: audio.speaker.bind("volume"),
      }).hook(audio.speaker, function (bar) {
        bar.class_name = audio.speaker.stream.isMuted ? "muted" : "";
      }),
    ];

    return true;
  },
  update: function () {
    var current_state = [audio.speaker.isMuted, audio.speaker.volume];
    if (
      current_state[0] === last_state[0] &&
      current_state[1] === last_state[1]
    ) {
      return false;
    }

    last_state = current_state;
    return true;
  },
});
