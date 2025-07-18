const notifications = await Service.import("notifications");
import { addToggle, setFill } from "./sidebar.js";

import Pango from "gi://Pango";

notifications.clearDelay = 15;
notifications.popupTimeout = 5000;

const DEFAULT_ICON = "dialog-information-symbolic";
var window;

export function get_monitor() {
  if (window === undefined) return -1;
  return window.monitor;
}

export function set_monitor(m) {
  window.monitor = m;
}

function NotificationIcon(notification) {
  // For some reason, the app-name set via `--icon` is coming in as image, so
  //   detect this and treat it as the `app_entry` property
  if (notification.image && Utils.lookUpIcon(notification.image)) {
    return Widget.Box({
      class_name: "image",
      child: Widget.Icon(notification.image),
    });
  }
  if (notification.image) {
    return Widget.Box({
      class_name: "image",
      css: `background-image: url("${notification.image}");`,
    });
  }
  if (notification.app_entry && Utils.lookUpIcon(notification.app_entry)) {
    return Widget.Box({
      class_name: "image",
      child: Widget.Icon(notification.app_entry),
    });
  }

  const icon_info = Utils.lookUpIcon(notification.app_icon);
  return Widget.Box({
    class_name: "image",
    child: Widget.Icon(icon_info ? notification.app_icon : DEFAULT_ICON),
  });
}

function build_notification(notification, persistent) {
  const icon = Widget.Box({
    vpack: "start",
    hexpand: false,
    class_name: "icon",
    child: NotificationIcon(notification),
  });

  const title = Widget.Label({
    class_name: "summary",
    xalign: 0,
    justification: "left",
    hexpand: true,
    max_width_chars: 24,
    truncate: "end",
    wrap: true,
    use_markup: true,
    label: notification.summary,
  });

  const body = Widget.Box({
    vpack: "start",
    hexpand: true,
    vexpand: true,
    children: [
      Widget.Label({
        class_name: "body-text",
        hexpand: true,
        vexpand: true,
        xalign: 0,
        justification: "left",
        wrap: true,
        wrap_mode: Pango.WrapMode.WORD_CHAR,
        use_markup: true,
        label: notification.body,
      }),
    ],
  });

  var box; // Hold a reference to the top level box for destruction purposes
  const actions = Widget.Box({
    class_name: "actions",
    children: notification.actions.map(function (action) {
      // WebCord sets an action that doesn't work, so just don't show it
      if (notification.app_name === "WebCord" && action.id === "default") {
        return;
      }
      return Widget.Button({
        class_name: "action",
        cursor: "pointer",
        hexpand: true,
        on_clicked: function (_) {
          // If you are not getting actions invoked from notifications, it probably
          //   means the launching program isn't registered correctly on dbus/with
          //   gtk
          console.log(`Invoking ${action.id} for ${notification.id}`);
          notification.invoke(action.id);
          if (
            // Resident means that the notification sticks around after actions
            notification.hints.resident &&
            notification.hints.resident.get_boolean()
          ) {
            return;
          }
          // Persistent instances need close, dismiss is for popups
          if (persistent) {
            if (box) box.destroy();
            notification.close();
          } else notification.dismiss();
        },
        child: Widget.Label(action.label),
      });
    }),
  });

  box = Widget.Box({
    class_name: `notification ${notification.urgency}`,
    vertical: true,
    vpack: "start",
    hexpand: true,
    vexpand: true,
    children: [
      Widget.Box({
        vexpand: true,
        vpack: "start",
        children: [
          icon,
          Widget.Box({
            orientation: 1,
            hexpand: true,
            vpack: "start",
            class_name: "text",
            children: [title, body],
          }),
        ],
      }),
      actions,
    ],
  });
  return box;
}

function NotificationPopup(notification) {
  // If dnd is turned on, skip any popups.  There is a weird scenario here where
  //   transient notifications just flat out get eaten, but that's probably fine.
  if (notifications.dnd) {
    return undefined;
  }

  return Widget.Revealer({
    transition: "slide_down",
    transitionDuration: 150,
    attribute: { id: notification.id },
    child: Widget.EventBox({
      on_secondary_click: function (_) {
        notification.dismiss();
      },
      hexpand: true,
      child: build_notification(notification, false),
    }),
  });
}

function NotificationWindow(notification) {
  // There shouldn't be any transient notifications in here, but if there are, just
  // skip them, transient means the notification shouldn't persist beyond the popup
  if (
    notification.hints.transient &&
    notification.hints.transient.get_boolean()
  ) {
    notification.close();
    return undefined;
  }

  const popup = build_notification(notification, true);
  return Widget.EventBox({
    hexpand: true,
    on_secondary_click: function (_) {
      notification.close();
      popup.destroy();
    },
    child: popup,
  });
}

addToggle({
  icon: notifications.bind("dnd").as(function (dnd) {
    return dnd ? "󰂛" : "󰂚";
  }),
  tooltip: notifications.bind("dnd").as(function (dnd) {
    return dnd ? "Show Notification Popups" : "Suppress Notification Popups";
  }),
  get_state: function () {
    return !notifications.dnd;
  },
  set_state: function (s) {
    notifications.dnd = !s;
  },
});

setFill(function () {
  return Widget.Box({
    class_name: "notifications-history",
    vertical: true,
    homogeneous: false,
    vexpand: true,
    hexpand: false,
    vpack: "start",
    // TODO: put button at top for clearing history
    children: [...notifications.notifications.map(NotificationWindow)],
  });
});

export default function setup_notifications(monitor = 0) {
  const notificationList = Widget.Box({
    vertical: true,
    children: notifications.popups.map(NotificationPopup),
  });

  notificationList.hook(
    notifications,
    function (_, id) {
      const notification = notifications.getNotification(id);
      if (notification) {
        // If the timeout is 1ms, just skip displaying it.  This is useful for any
        //   scenarios where we want something to live in the persistent list but
        //   not interrupt the user, like long lived actions
        if (notification.timeout === 1) {
          notification.dismiss();
          return;
        }

        const notificationPopup = NotificationPopup(notification);
        if (notificationPopup === undefined) return;
        notificationList.children = [
          notificationPopup,
          ...notificationList.children,
        ];
        Utils.timeout(notification.timeout + 5, notification.dismiss);
        Utils.timeout(5, function () {
          notificationPopup.reveal_child = true;
        });
      }
    },
    "notified",
  );
  notificationList.hook(
    notifications,
    function (_, id) {
      const popup = notificationList.children.find(function (popup) {
        if (!popup.attribute) return;
        return popup.attribute.id === id;
      });
      // Get the persistent notification object, if it's marked as transient, it
      //   shouldn't persist, so close the persistent one once this is dismissed.
      //   We need to wait for dismissal, otherwise we signal to anything awaiting
      //   actions that it's closed w/o actions and they don't get invoked
      const non_popup = notifications.notifications.find(function (n) {
        return n.id === id;
      });
      if (
        non_popup &&
        non_popup.hints.transient &&
        non_popup.hints.transient.get_boolean()
      )
        non_popup.close();

      if (popup) {
        // We want to animate the removal, but in order to avoid the animation being
        //   triggered twice, we blank the lookup attribute in order to effectively
        //   orphan the widget while it goes through the state transition to gc
        //   itself
        popup.attribute.id = null;
        Utils.timeout(popup.transitionDuration, function () {
          popup.destroy();
        });
        popup.reveal_child = false;
      }
    },
    "dismissed",
  );

  window = Widget.Window({
    name: "ags.notifications",
    class_name: "notification-popups",
    monitor,
    anchor: ["top", "right"],
    child: Widget.Box({
      class_name: "notifications",
      css: "min-height: 2px; min-width: 2px;",
      vertical: true,
      child: notificationList,
    }),
  });

  return window;
}
