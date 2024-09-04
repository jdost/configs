const osd_container = Widget.Box({
  class_name: "osd",
  css: "min-height: 2px; min-width: 2px;",
});
let hook_register = [];
let active_hook = null;
let active_timeout = null;

export default function build_window(monitor = 0) {
  // Hooks trigger on load, causing noise on launch, so silence them for .5s on launch
  Utils.timeout(500, function finish_hook_init() {
    hook_register.map(function (hook) {
      hook.has_init = true;
    });
  });

  return Widget.Window({
    name: "ags.osd",
    monitor,
    anchor: ["bottom"],
    exclusivity: "ignore",
    child: osd_container,
  });
}

function set_window(hook) {
  if (active_hook) {
    osd_container.child.destroy();
  } else if (osd_container.child) {
    // There is a child but the active isn't agreeing
    console.log("Oops, why is the tracker out of sync?");
    return;
  }
  osd_container.child = hook.widget;
  active_hook = hook;
  refresh_window_timeout(hook.timeout);
}

function refresh_window_timeout(timeout = 2000) {
  if (active_timeout) {
    active_timeout.destroy();
  }
  active_timeout = setTimeout(function () {
    active_timeout = null;
    active_hook = null;
    osd_container.child.destroy();
  }, timeout);
}

export function register_hook(obj, handler, signal) {
  const name = obj.name || `${obj.hook[0].name}-${obj.hook[1]}`;
  if (!obj.setup) {
    console.log("Need to define a `setup` handler!");
    return;
  }
  let self = {
    name: name,
    widget: null,
    timeout: obj.timeout || 2000,
    hook: obj.hook,
    has_init: false,
    setup: obj.setup,
    update:
      obj.update ||
      function (_) {
        return true;
      },
    widget_props: obj.properties || {},
  };
  self.handler = function (window) {
    if (!self.has_init) {
      return;
    }

    if (!self.widget) {
      self.widget = Widget.Box({
        class_name: self.name,
        ...self.widget_props,
      });
      self.widget.on("destroy", function () {
        self.widget = null;
      });
      if (self.setup(self.widget)) {
        set_window(self);
      } else {
        self.widget.destroy();
      }
    } else if (!self.update(self)) {
      return;
    } else {
      refresh_window_timeout(self.timeout);
    }
  };

  osd_container.hook(self.hook[0], self.handler, self.hook[1]);
  hook_register.push(self);
}
