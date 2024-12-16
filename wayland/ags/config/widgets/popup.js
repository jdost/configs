import GLib from 'gi://GLib'

export function Popup(obj) {
  if (!obj.setup) {
    console.log("Need to define a `setup` handler!");
    return;
  }
  if (!obj.name) {
    console.log("Need to define a `name` for this popup!");
    return;
  }

  let timeout_handler = null;
  let self = {
    name: obj.name,
    widget: null,
    setup: obj.setup,
    timeout: obj.timeout,
  };

  function close_popup() {
    if (self.widget === null)
      return

    if (timeout_handler !== null) {
      GLib.source_remove(timeout_handler);
      timeout_handler = null;
    }

    self.widget.close();
    self.widget = null;
    return;
  };

  self.toggle = function () {
    if (self.widget !== null) {
      return close_popup();
    }

    self.widget = Widget.Window({
      name: `ags.popup.${self.name}`,
      class_name: `popup ${self.name}`,
      anchor: ["top", "right"],
      setup: self.setup,
    });

    // If a timeout is specified, auto close the popup after it's elapsed
    if (self.timeout !== undefined) {
      timeout_handler = Utils.timeout(self.timeout, close_popup);
    }

    return self.widget;
  };

  return self;
};
