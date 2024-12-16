const mpris = await Service.import("mpris");
import { add_icon } from "../widgets/bar.js";
import { Popup } from "../widgets/popup.js";

const name_icons = {
  spotify: ["󰓇", "rgb(30, 215, 96)"],
  spotifyd: ["󰓇", "rgb(30, 215, 96)"],
  firefox: ["󰈹", "rgb(230, 96, 0)"],
  chromium: ["", "rgb(0, 136, 247)"],
  mpv: ["󰐌", "rgb(160, 60, 210)"],
};
const default_icon = "󰝚";
let tracking_file = "";
const bus_offset = "org.mpris.MediaPlayer2.".length
Utils.execAsync(["id", "-u"])
  .then(function (output) {
    tracking_file = `/run/user/${output}/mpris-tracker`
    Utils.execAsync(["touch", tracking_file]);
  });

const player_tracker = {
  players: {},
  active: undefined,
  icon: undefined,

  _update () {
    if (this.icon === undefined)
      return;

    let playing = [];
    let latest_non_player = undefined;
    for (const bus_name in this.players) {
      const player = this.players[bus_name];
      if (player.playback_status() === "playing")
        playing.push(player);
      else if (latest_non_player === undefined)
        latest_non_player = player;
      else if (latest_non_player.last_update < player.last_update)
        latest_non_player = player;
    }
    this.icon.toggleClassName("not-playing", playing.length === 0);
    if (playing.length > 1) {
      playing.sort(function (a, b) { return b.last_update - a.last_update; });
      this.active = playing[0];
      for (i = 1; i < playing.length; i++) {
        console.log("would pause:", playing[1].toString());
      }
    } else if (playing.length === 1) {
      this.active = playing[0];
    } else if (latest_non_player !== undefined) {
      this.active = latest_non_player;
    } else {
      this.active = undefined;
      this.icon.label = "?";
      return;
    }

    this.icon.label = this.active.icon();
    if (this.active.playback_status() === "playing")
      this.icon.css = `color: ${playing[0].color()}`;
    else
      this.icon.css = "";
    if (tracking_file)
      Utils.writeFile(this.active.instance_name, tracking_file);
  },

  add (bus_name) {
    if (bus_name == undefined)
      return "undefined";
    // This is likely impossible... but be defensive
    if (this.players[bus_name])
      return this.players[bus_name];
    this.players[bus_name] = new Player(bus_name);
    this._update();
    return this.players[bus_name];
  },

  update (bus_name) {
    if (bus_name == undefined)
      return "undefined";
    if (this.players[bus_name] === undefined)
      return `doesnt exist ${bus_name}`;
    this.players[bus_name].update();
    this._update();
    return this.players[bus_name];
  },

  remove (bus_name) {
    if (this.players[bus_name])
      delete this.players[bus_name];

    this._update();
  }
};


class Player {
  constructor (bus_name) {
    this.bus_name = bus_name;
    this.instance_name = bus_name.substring(bus_offset);
    this.last_update = (new Date()).valueOf();
    this.last_status = this.playback_status();
  }

  update () {
    // If the playback status doesn't change, don't consider it an update
    if (this.last_status === this.playback_status())
      return;
    this.last_status = this.playback_status();
    this.last_update = (new Date()).valueOf();
  }

  toString () {
    const player = this.getPlayer();
    return `Player<${this.instance_name}> - ${player.name}: ${player.play_back_status}`
  }

  playback_status () {
    return this.getPlayer().play_back_status.toLowerCase();
  }

  getPlayer () {
    return mpris.getPlayer(this.bus_name);
  }

  icon () {
    const name = this.getPlayer().name;
    return name_icons[name][0] || default_icon;
  }

  color () {
    const name = this.getPlayer().name;
    return name_icons[name][1] || "rgb(255, 255, 255)";
  }
}

const popup = Popup({
  name: "mpris",
  setup: function (window) {
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
      label: player.bind("track_artists").transform(function (a) { return a.join(", "); }),
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
                    on_clicked: function (_) { player.previous(); },
                    visible: player.bind("can_go_prev"),
                    cursor: "pointer",
                    child: Widget.Icon("media-skip-backward-symbolic"),
                  }),
                  Widget.Button({
                    class_name: "play-pause",
                    on_clicked: function (_) { console.log("pp triggered"); player.playPause(); },
                    visible: player.bind("can_play"),
                    cursor: "pointer",
                    child: Widget.Icon({
                      icon: player.bind("play_back_status").transform(function (s) {
                        switch (s) {
                          case "Playing": return "media-playback-pause-symbolic";
                          case "Paused":
                          case "Stopped": return "media-playback-start-symbolic";
                        }
                      }),
                    }),
                  }),
                  Widget.Button({
                    on_clicked: function (_) { player.next(); },
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

add_icon(
  Widget.EventBox({
    class_name: "mpris",
    on_primary_click: function (_, e) {
      return popup.toggle();
    },
    child: Widget.Label({
      setup: function (icon) {
        player_tracker.icon = icon;
        icon.hook(mpris, function (self, player) {
          console.log("new", player_tracker.add(player).toString());
        }, "player-added");
        icon.hook(mpris, function (self, player) {
          player_tracker.remove(player);
          console.log("rm", player);
        }, "player-closed");
        icon.hook(mpris, function (self, player) {
          console.log("update", player_tracker.update(player).toString());
        }, "player-changed");
      },
    }),
  }),
  5,
);
