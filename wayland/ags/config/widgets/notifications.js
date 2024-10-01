const notifications = await Service.import("notifications");
notifications.clearDelay = 15;
notifications.popupTimeout = 5000;

const DEFAULT_ICON = "dialog-information-symbolic";

function NotificationIcon(notification) {
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

function NotificationPopup(notification) {
  const icon = Widget.Box({
    vpack: "start",
    hexpand: false,
    class_name: "icon",
    child: NotificationIcon(notification),
  });

  const title = Widget.Label({
    class_name: "title",
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
    vpack: 'start',
    hexpand: true,
    vexpand: true,
    children: [
      Widget.Label({
        class_name: "body",
        hexpand: true,
        vexpand: true,
        xalign: 0,
        justification: "left",
        wrap: true,
        use_markup: true,
        label: notification.body,
      }),
    ],
  });

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
          console.log(`Invoking ${action.id} for ${notification.id}`);
          notification.invoke(action.id);
          notification.dismiss();
        },
        child: Widget.Label(action.label),
      });
    }),
  });

  return Widget.Revealer({
    transition: "slide_down",
    transitionDuration: 150,
    attribute: { id: notification.id },
    child: Widget.EventBox({
      on_primary_click: notification.dismiss,
      hexpand: true,
      child: Widget.Box({
        class_name: `notification ${notification.urgency}`,
        vertical: true,
        vpack: 'start',
        hexpand: true,
        vexpand: true,
        children: [
          Widget.Box({
            vexpand: true,
            vpack: 'start',
            children: [
              icon,
              Widget.Box({
                orientation: 1,
                hexpand: true,
                vpack: 'start',
                class_name: 'text',
                children: [title, body],
              }),
            ],
          }),
          actions,
        ],
      }),
    }),
  });
}


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
        const notificationPopup = NotificationPopup(notification)
        notificationList.children = [
          notificationPopup,
          ...notificationList.children,
        ]
        Utils.timeout(notification.timeout + 5, notification.dismiss);
        Utils.timeout(5, function () { notificationPopup.reveal_child = true; });
      }
    },
    "notified",
  );
  notificationList.hook(
    notifications,
    function (_, id) {
      notificationList.children
        .find(function (popup) {
          if (!popup.attribute) { return; }
          if (popup.attribute.id === id)  // TODO remove
            console.log(`Dismissing: ${id}`);
          return popup.attribute.id === id;
        })
        ?.destroy();
    },
    "dismissed",
  );

  return Widget.Window({
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
}
