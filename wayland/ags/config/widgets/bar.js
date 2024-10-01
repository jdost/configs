let LeftWidgets = [];
let RightWidgets = {
  before: [],
  icons: [],
  after: [],
};

export function add_left(widget) {
  LeftWidgets.push(widget);
}

export function add_right(widget, before_icons) {
  if (before_icons) {
    RightWidgets.before.push(widget);
  } else {
    RightWidgets.after.push(widget);
  }
}

export function add_icon(icon, priority = 0) {
  Object.assign(icon, {
    priority: priority,
  });
  RightWidgets.icons.push(icon);
}

export default function build_bar(monitor = 0) {
  return Widget.Window({
    name: `ags.bar.${monitor}`,
    class_name: "bar",
    monitor,
    anchor: ["top", "left", "right"],
    exclusivity: "exclusive",
    cursor: "default",
    child: Widget.CenterBox({
      start_widget: Widget.Box({
        hpack: "start",
        class_name: "left",
        children: LeftWidgets,
      }),
      end_widget: Widget.Box({
        hpack: "end",
        class_name: "right",
        children: [
          ...RightWidgets.before,
          Widget.Box({
            hpack: "start",
            class_name: "icons",
            spacing: 6,
            children: RightWidgets.icons.toSorted(function (a, b) {
              const a_prio = a.priority || -1;
              const b_prio = b.priority || -1;
              if (a_prio == b_prio)
                return a.class_name.localeCompare(b.class_name);
              return b_prio - a_prio;
            }),
          }),
          ...RightWidgets.after,
        ],
      }),
    }),
  });
}
