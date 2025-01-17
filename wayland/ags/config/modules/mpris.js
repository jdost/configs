const mpris = await Service.import("mpris");
import { addIcon } from "../widgets/bar.js";
import { Popup } from "../widgets/popup.js";
import { addBlock } from "../widgets/sidebar.js";

const name_icons_text = {
  spotify: ["󰓇", "rgb(30, 215, 96)"],
  spotifyd: ["󰓇", "rgb(30, 215, 96)"],
  firefox: ["󰈹", "rgb(230, 96, 0)"],
  chromium: ["", "rgb(0, 136, 247)"],
  mpv: ["󰐌", "rgb(200, 100, 255)"],
};
const name_icons = {
  spotify: "spotify",
  spotifyd: "spotify",
  firefox: "firefox",
  chromium: "chromium",
  mpv: "mpv",
};
const default_icon_text = "󰝚";
let tracking_file = "";
const bus_offset = "org.mpris.MediaPlayer2.".length;
const NOT_PLAYING_COLOR = "rgb(153, 153, 153)";
Utils.execAsync(["id", "-u"]).then(function (output) {
  tracking_file = `/run/user/${output}/mpris-tracker`;
  Utils.execAsync(["touch", tracking_file]);
});

const player_tracker = {
  players: {},
  active: undefined,
  icon: undefined,

  _update() {
    if (this.icon === undefined) return;

    let playing = [];
    let latest_non_player = undefined;
    for (const bus_name in this.players) {
      const player = this.players[bus_name];
      if (player.playback_status() === "playing") playing.push(player);
      else if (latest_non_player === undefined) latest_non_player = player;
      else if (latest_non_player.last_update < player.last_update)
        latest_non_player = player;
    }
    this.icon.toggleClassName("not-playing", playing.length === 0);
    if (playing.length > 1) {
      playing.sort(function (a, b) {
        return b.last_update - a.last_update;
      });
      this.active = playing[0];
      for (var i = 1; i < playing.length; i++) {
        console.log("would pause:", playing[1].toString());
      }
    } else if (playing.length === 1) {
      this.active = playing[0];
    } else if (latest_non_player !== undefined) {
      this.active = latest_non_player;
    } else {
      this.active = undefined;
      this.icon.label = default_icon;
      this.icon.css = "color: #999999;";
      return;
    }

    this.icon.label = this.active.icon();
    this.icon.css =
      this.active.playback_status() === "playing"
        ? `color: ${playing[0].color()}`
        : `color: ${NOT_PLAYING_COLOR}`;
    this.icon.tooltip_text = this.active.tooltip();
    if (tracking_file)
      Utils.writeFile(this.active.instance_name, tracking_file);
  },

  add(bus_name) {
    if (bus_name == undefined) return "undefined";
    // This is likely impossible... but be defensive
    if (this.players[bus_name]) return this.players[bus_name];
    this.players[bus_name] = new Player(bus_name);
    this._update();
    console.log(`Player Added: ${this.players[bus_name].toString()}`);
    return this.players[bus_name];
  },

  update(bus_name) {
    if (bus_name == undefined) return "undefined";
    if (this.players[bus_name] === undefined) return `doesnt exist ${bus_name}`;
    if (this.players[bus_name].update())
      console.log(`Player Updated: ${this.players[bus_name].toString()}`);

    this._update();
    return this.players[bus_name];
  },

  remove(bus_name) {
    if (bus_name == undefined) return;
    if (this.players[bus_name]) delete this.players[bus_name];

    this._update();
    console.log(
      `Player Removed: ${bus_name}, active: ${this.active.toString()}`,
    );
  },
};

class Player {
  constructor(bus_name) {
    this.bus_name = bus_name;
    this.instance_name = bus_name.substring(bus_offset);
    this.last_update = new Date().valueOf();
    this.last_status = this.playback_status();
  }

  update(force) {
    if (!force) {
      // If the playback status doesn't change, don't consider it an update
      if (this.last_status === this.playback_status()) return false;
      this.last_status = this.playback_status();
    }
    this.last_update = new Date().valueOf();
    return true;
  }

  toString() {
    const player = this.getPlayer();
    return `Player<${this.instance_name}> - ${player.name}: ${player.play_back_status}`;
  }

  playback_status() {
    return (this.getPlayer().play_back_status || "stopped").toLowerCase();
  }

  getPlayer() {
    return mpris.getPlayer(this.bus_name);
  }

  icon(as_icon) {
    const name = this.getPlayer().name;
    if (as_icon)
      return name_icons[name] || default_icon;
    else return name_icons_text[name][0] || default_icon_text;
  }

  color() {
    const name = this.getPlayer().name;
    return name_icons_text[name][1] || "rgb(255, 255, 255)";
  }

  tooltip() {
    const player = this.getPlayer();
    return `${player.name} - ${player.play_back_status}`;
  }

  name() {
    return this.getPlayer().name;
  }
}

const popup = Popup({
  name: "mpris",
  timeout: 5000,
  setup: function (window) {
    if (player_tracker.active === undefined) return false;
    const player = player_tracker.active.getPlayer();
    if (player === undefined) {
      console.log("No active player...");
      return false;
    }

    const cover_art = Widget.Box({
      class_name: "cover-art",
      vpack: "start",
      css: player.bind("cover_path").transform(function (p) {
        return `background-image: url('${p}');`;
      }),
    });

    const artists = Widget.Label({
      class_name: "artist",
      truncate: "end",
      hpack: "start",
      label: player.bind("track_artists").transform(function (a) {
        return a.join(", ");
      }),
    });

    window.child = Widget.Box({
      children: [
        cover_art,
        Widget.Box({
          vertical: true,
          hexpand: true,
          children: [
            Widget.Box({
              children: [
                Widget.Label({
                  class_name: "title",
                  truncate: "end",
                  hpack: "start",
                  label: player.bind("track_title"),
                }),
              ],
            }),
            artists,
            Widget.Box({ vexpand: true }),
            Widget.CenterBox({
              center_widget: Widget.Box({
                children: [
                  Widget.Button({
                    on_clicked: function (_) {
                      player.previous();
                    },
                    visible: player.bind("can_go_prev"),
                    cursor: "pointer",
                    child: Widget.Icon("media-skip-backward-symbolic"),
                  }),
                  Widget.Button({
                    class_name: "play-pause",
                    on_clicked: function (_) {
                      player.playPause();
                    },
                    visible: player.bind("can_play"),
                    cursor: "pointer",
                    child: Widget.Icon({
                      icon: player
                        .bind("play_back_status")
                        .transform(function (s) {
                          switch (s) {
                            case "Playing":
                              return "media-playback-pause-symbolic";
                            case "Paused":
                            case "Stopped":
                              return "media-playback-start-symbolic";
                          }
                        }),
                    }),
                  }),
                  Widget.Button({
                    on_clicked: function (_) {
                      player.next();
                    },
                    visible: player.bind("can_go_next"),
                    cursor: "pointer",
                    child: Widget.Icon("media-skip-forward-symbolic"),
                  }),
                ],
              }),
            }),
          ],
        }),
      ],
    });
  },
});

addIcon(
  Widget.EventBox({
    class_name: "mpris",
    on_primary_click: function (_, e) {
      return popup.toggle();
    },
    on_secondary_click: function (_, e) {
      var items = [];
      const self = player_tracker; // Alias `this` to avoid conflict in callbacks

      for (const bus_name in self.players) {
        items.push(
          Widget.MenuItem({
            class_name: self.players[bus_name] === self.active ? "active" : "",
            on_activate: function () {
              console.log(`Bumping ${bus_name} to active`);
              self.players[bus_name].update(true);
              self._update();
            },
            cursor: "pointer",
            child: Widget.Label({
              justification: "left",
              xalign: 0,
              label: self.players[bus_name].name(),
            }),
          }),
        );
      }

      const menu = Widget.Menu({
        class_name: "mpris-select",
        children: items,
        reserve_toggle_size: false,
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
    child: Widget.Label({
      label: default_icon_text,
      css: "color: #999999;",
      setup: function (icon) {
        player_tracker.icon = icon;
        icon.hook(
          mpris,
          function (self, player) {
            player_tracker.add(player);
          },
          "player-added",
        );
        icon.hook(
          mpris,
          function (self, player) {
            player_tracker.remove(player);
          },
          "player-closed",
        );
        icon.hook(
          mpris,
          function (self, player) {
            player_tracker.update(player);
          },
          "player-changed",
        );
      },
    }),
  }),
  5,
);

addBlock(function () {
  if (player_tracker.active === undefined) return undefined;
  if (player_tracker.active.playback_status() !== "playing") return undefined;

  const player = player_tracker.active.getPlayer();
  return Widget.CenterBox({
    centerWidget: Widget.Box({
      class_name: "mpris",
      homogeneous: false,
      vpack: "start",
      hexpand: false,
      children: [
        Widget.Icon(player_tracker.active.icon(true)),
        Widget.Label({
          label: player.bind('track_artists').as(function (a) {
            return a.join(", ");
          }),
        }),
        Widget.Label("-"),
        Widget.Label({
          truncate: "end",
          label: player.bind('track_title'),
        }),
      ],
    })
  });
});
