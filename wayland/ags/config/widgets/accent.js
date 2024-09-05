export default function build_accent(monitor = 0) {
  return Widget.Window({
    name: "ags.accent",
    class_name: "accent",
    monitor,
    exclusivity: "ignore",
    anchor: ["top", "left", "right"],
    child: Widget.CenterBox({
      center_widget: Widget.Box({
        children: [],
      }),
    }),
  });
}
