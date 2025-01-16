const audio = await Service.import("audio");
import { LevelDots } from "../widgets/icons.js";
import { addIcon } from "../widgets/bar.js";
import { register_hook } from "../widgets/osd.js";
import { Popup } from "../widgets/popup.js";
import { addToggle } from "../widgets/sidebar.js";

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

const popup = Popup({
  name: "audio",
  timeout: 10000,
  setup: function (window) {
    function StreamSlider(stream) {
      const button = Widget.Button({
        cursor: "pointer",
        tooltip_text: stream.bind("is_muted") ? "Unmute" : "Mute",
        child: Widget.Icon({
          icon: stream.bind("volume").as(function (v) {
            if (v > 0.66) return "audio-volume-high-symbolic";
            else if (v > 0.33) return "audio-volume-medium-symbolic";
            else if (v > 0) return "audio-volume-low-symbolic";
            return "audio-volume-muted-symbolic";
          }),
        }),
        class_name: stream.is_muted ? "" : "active",
        onClicked: function (e) {
          stream.is_muted = !stream.is_muted;
          button.toggleClassName("active");
        },
      });
      const label = stream.stream.port
        ? stream.description
        : `${stream.stream.name}: ${stream.stream.description}`;
      return Widget.Box({
        name: `audio.slider.${stream.name}`,
        class_name: stream.stream.port
          ? "audio-slider device"
          : "audio-slider app",
        children: [
          button,
          Widget.Box({
            vertical: true,
            children: [
              Widget.Box({
                children: [
                  Widget.Label({
                    class_name: "name",
                    hexpand: true,
                    truncate: "end",
                    hpack: "start",
                    label: label,
                  }),
                  Widget.Label({
                    class_name: "volume",
                    label: stream.bind("volume").as(function (v) {
                      return `${Math.trunc(v * 100)}%`;
                    }),
                  }),
                ],
              }),
              Widget.Slider({
                hexpand: true,
                drawValue: false,
                cursor: "pointer",
                onChange: function (slider) {
                  stream.volume = slider.value;
                },
                value: stream.bind("volume"),
              }),
            ],
          }),
        ],
      });
    }
    let sliders = [
      Widget.Label({ class_name: "header", label: "Volume Controls" }),
      StreamSlider(audio.speaker),
    ];
    audio.apps.forEach(function (app) {
      sliders.push(StreamSlider(app));
    });

    window.child = Widget.Box({
      vertical: true,
      children: sliders,
    });
  },
});

addIcon(
  Widget.EventBox({
    class_name: "audio",
    child: Widget.Box({
      spacing: 0,
      children: [LevelDots(audio.speaker), LevelDots(audio.microphone)],
    }),
    on_primary_click: function (_, e) {
      popup.toggle();
    },
    on_secondary_click: function (_, e) {
      const sources = Widget.MenuItem({
        child: Widget.Label({
          hpack: "start",
          label: "Inputs",
        }),
      });
      const sourcesMenu = Widget.Menu({
        class_name: "audio-select",
        reserve_toggle_size: false,
        children: audio.microphones.map(function (source) {
          return Widget.MenuItem({
            on_activate: function () {
              console.log(`Changing ${source.description} to default input`);
              audio.microphone = source;
            },
            class_name: source.id === audio.microphone.id ? "active" : "",
            child: Widget.Label({
              hpack: "start",
              label: source.description,
            }),
          });
        }),
      });
      sources.set_submenu(sourcesMenu);

      const sinks = Widget.MenuItem({
        child: Widget.Label({
          hpack: "start",
          label: "Outputs",
        }),
      });
      const sinksMenu = Widget.Menu({
        class_name: "audio-select",
        reserve_toggle_size: false,
        children: audio.speakers.map(function (sink) {
          return Widget.MenuItem({
            on_activate: function () {
              console.log(`Changing ${sink.description} to default output`);
              audio.speaker = sink;
            },
            class_name: sink.id === audio.speaker.id ? "active" : "",
            child: Widget.Label({
              hpack: "start",
              label: sink.description,
            }),
          });
        }),
      });
      sinks.set_submenu(sinksMenu);

      const menu = Widget.Menu({
        class_name: "audio-select",
        reserve_toggle_size: false,
        children: [sinks, sources],
      });

      // AGS doesn't auto set this up, so hook the deactivate, which is triggered
      //  when you click out of the menu and it goes away, so destroy the objects
      menu.connect("deactivate", function (e) {
        // Set the destroy on a timeout since this triggers before the menu item's
        //   activate event, making the actual selection never happen
        setTimeout(function () {
          menu.destroy();
        }, 10);
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

addToggle({
  icon: audio.microphone.bind("is_muted").as(function (muted) {
    return muted ? "󰍭" : "󰍬";
  }),
  tooltip: audio.microphone.bind("is_muted").as(function (muted) {
    return muted ? "Unmute Microphone" : "Mute Microphone";
  }),
  get_state: function () {
    return !audio.microphone.is_muted;
  },
  set_state: function (s) {
    audio.microphone.is_muted = !s;
  },
});
