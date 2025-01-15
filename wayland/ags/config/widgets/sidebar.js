// The sidebar is made of three types of widgets, the blocks, which are generic,
//   large widgets like the calendar, toggles which are small buttons that hook into
//   helper controls like notification DnD, and then the fill widget, which is
//   normally going to be the notification history and just takes up the rest of the
//   sidebar.
let Widgets = {
  blocks: [],
  toggles: [],
  fill: undefined,
};

let bar = undefined;

export function addBlock(builder) {
  // blocks are just functions that generate a base Widget that gets included in
  //   the sidebar
  Widgets.blocks.push(builder);
}

export function setFill(builder) {
  // the fill is also just a function that generates a base widget that gets
  //   included in the sidebar, but there should only be one
  if (Widgets.fill !== undefined) {
    console.log("Sidebar Fill already defined!");
    return;
  }

  Widgets.fill = builder;
}

export function addToggle(settings) {
  // Toggles are an object with some basic settings:
  //   icon - A string with (expected) a single character from something like
  //     nerd font for the label of the toggle button
  //   tooltip - A string that gives a longer description of the toggle
  //   set_state - A function/callback that takes the new state and is run on toggle
  //   get_state - A function that returns a boolean on whether the toggle should be
  //     on or not
  Widgets.toggles.push(settings);
}

function buildToggles() {
  if (Widgets.toggles.length === 0) return undefined;
  return Widget.Box({
    class_name: "toggles",
    hpack: "center",
    spacing: 5,
    children: Widgets.toggles.map(function (toggle) {
      return Widget.ToggleButton({
        class_name: "toggle",
        active: toggle.get_state(),
        cursor: "pointer",
        onToggled: function (w) {
          toggle.set_state(w.active);
        },
        child: Widget.Label({ label: toggle.icon }),
        tooltip_text: toggle.tooltip,
      });
    }),
  });
}

function build_bar() {
  // Wrap the actual bar in a revealer for a nice animation
  const revealer = Widget.Revealer({
    transition: "slide_left",
    transitionDuration: 200,
    child: Widget.Scrollable({
      hscroll: "never",
      vscroll: "automatic",
      child: Widget.Box({
        vertical: true,
        homogeneous: false,
        children: [
          ...Widgets.blocks.map(function (block) {
            return block();
          }),
          buildToggles(),
          Widgets.fill !== undefined ? Widgets.fill() : null,
        ],
      }),
    }),
  });

  const window = Widget.Window({
    name: "ags.sidebar",
    anchor: ["top", "right", "bottom"],
    cursor: "default",
    css: "background-color: transparent;",
    exclusivity: "normal",
    child: Widget.Box({
      class_name: "sidebar",
      css: "min-width: 1px;",
      child: revealer,
    }),
    setup: function () {
      Utils.timeout(100, function () {
        revealer.reveal_child = true;
      });
    },
  });

  return window;
}

export function toggle() {
  if (bar === undefined) {
    bar = build_bar();
  } else {
    const revealer = bar.child.child;
    revealer.reveal_child = false;
    Utils.timeout(revealer.transitionDuration, function () {
      bar.close();
      bar = undefined;
    });
  }
}
