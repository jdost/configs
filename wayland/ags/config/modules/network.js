/*
- show primary as base icon
- tooltip SSID if wifi
- badge bound to VPN
*/

const network = await Service.import("network");
const PHONE_WIFI_PREFIX = "Pixel_";
import { addIcon } from "../widgets/bar.js";
import { addToggle } from "../widgets/sidebar.js";

const wifiStrength = [..."󰤟󰤢󰤥󰤨"];
const vpnIcons = {
  connected: "󰳌",
  disconnected: "",
  connecting: "󱆣",
  disconnecting: "󰫝",
};

addIcon(
  Widget.Overlay({
    class_name: "network",
    pass_through: true,
    setup: function (self) {
      const icon = Widget.Label({
        label: "",
      });
      self.child = icon;

      const vpn_badge = Widget.Label({
        class_name: "badge",
        label: "",
      });
      self.overlays = [vpn_badge];

      Utils.merge(
        [
          network.bind("primary"),
          network.bind("wired"),
          network.bind("wifi"),
          network.bind("vpn"),
        ],
        function (primary, wired, wifi, vpn) {
          if (wired.state === "connected" || wired.state === "activated") {
            icon.label = "";
            self.tooltip_text = `Ethernet - ${wired.state}`;
          } else if (
            wifi.internet === "connected" ||
            wifi.state === "connected" ||
            wifi.state === "activated"
          ) {
            if (wifi.ssid.startsWith(PHONE_WIFI_PREFIX)) {
              // use different icon?
              // icon.label = "󰠕";
            }
            icon.label =
              wifiStrength[
                Math.round((wifi.strength / 100) * (wifiStrength.length - 1))
              ];
            self.tooltip_text = `${wifi.ssid} ${wifi.strength}%`;
          } else if (!wifi.enabled) {
            icon.label = "󰀝";
            self.tooltip_text = "";
          } else {
            icon.label = "󰤮";
            console.log(wifi.state);
            self.tooltip_text = "";
          }

          //console.log(vpn);
          if (!vpn) return;

          if (vpn.activated_connections.length > 0) {
            const vpn_conn = vpn.activated_connections[0]; // assume there's only one
            self.tooltip_text = `${self.tooltip_text} - VPN: ${vpn.id}`;
            vpn_badge.label = vpnIcons[vpn_conn.state];
          }
        },
      );
    },
  }),
  5,
);

if (network.wifi) {
  addToggle({
    icon: network.wifi.bind("enabled").as(function (en) {
      return en ? "󰖩" : "󰖪";
    }),
    tooltip: network.wifi.bind("enabled").as(function (en) {
      return en ? "Turn off Wifi Radio" : "Turn on Wifi Radio";
    }),
    get_state: function () { return network.wifi.enabled; },
    set_state: function (s) { network.wifi.enabled = s; },
  });
}
