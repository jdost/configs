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
    class_name: "icon",
    child: NotificationIcon(notification),
  });
  console.log(`Creating: ${notification.id} (timeout:${notification.timeout})`);

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

  const body = Widget.Label({
    class_name: "body",
    hexpand: true,
    xalign: 0,
    justification: "left",
    wrap: true,
    use_markup: true,
    label: notification.body,
  });

  const actions = Widget.Box({
    class_name: "actions",
    children: [],
    /*notification.actions.map(function (action) {
      return Widget.Button({
        class_name: "action",
        on_clicked: function (_) {
          notification.invoke(action.id);
          notification.dismiss();
        },
        child: Widget.Label(action.label),
      });
    }),*/
  });

  return Widget.EventBox({
    on_primary_click: notification.dismiss,
    attribute: { id: notification.id },
    child: Widget.Box({
      class_name: `notification ${notification.urgency}`,
      vertical: true,
      vexpand: true,
      children: [
        Widget.Box({
          children: [
            icon,
            Widget.Box({
              vertical: true,
              children: [title, body],
            }),
          ],
        }),
        actions,
      ],
    }),
  });
}

export default function setup_notifications(monitor = 0) {
  const notificationList = Widget.Box({
    class_name: "notifications",
    vertical: true,
    children: notifications.popups.map(NotificationPopup),
  });

  notificationList.hook(
    notifications,
    function (_, id) {
      const notification = notifications.getNotification(id);
      if (notification) {
        notificationList.children = [
          NotificationPopup(notification),
          ...notificationList.children,
        ];
      }
    },
    "notified",
  );
  notificationList.hook(
    notifications,
    function (_, id) {
      console.log(`Dismissing: ${id}`);
      const notification = notifications.getPopup(id);
      if (notification) {
        console.log(`Closing: ${notification.summary} (${id})`);
      }
      notificationList.children
        .find(function (popup) {
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
    child: notificationList,
    css: "min-height: 2px; min-width: 2px;",
  });
}
