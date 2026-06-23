pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Hyprland
import Quickshell.Services.Notifications

Singleton {
    id: notifications

    readonly property real defaultTimeout: 5000
    property bool dnd: false

    NotificationServer {
        id: server

        actionIconsSupported: true
        actionsSupported: true
        bodyHyperlinksSupported: false
        bodyImagesSupported: true
        bodyMarkupSupported: true
        bodySupported: true
        imageSupported: true
        persistenceSupported: true

        onNotification: function (notification) {
            notification.tracked = true;
            notification.createdAt = new Date().valueOf();
            notification.closedReason = -1;

            notifications.current.push(notification);
            if (notification.isExpired || notification.lastGeneration)
                return;
            notification.closed.connect(function (reason) {
                notification.closedReason = reason;
                console.log(`Notification ${notification.id} closed: ${reason}`);
                // Expiration should be cleaned up from the outputs, but not the history
                if (notification.output === undefined) {
                    return;
                }

                const output = notification.output;
                output.append({
                    "action": "remove",
                    "target": notification.id
                });

                const idx = notifications.current.indexOf(notification);
                if (idx === -1)
                    return;

                console.log(`Removing ${notification.id} from history...`);
                notifications.current.splice(idx, 1);
            });

            if (dnd)
                return;

            const output = notifications.getOutput(Hyprland.focusedMonitor.name);
            notification.output = output;
            output.append({
                "action": "add",
                "msg": notification
            });

            notification.timer = Qt.createQmlObject("import QtQuick 2.0; Timer {}", notifications);
            notification.timer.interval = notification.expireTimeout > 0 ? notification.expireTimeout : defaultTimeout;
            notification.timer.repeat = false;
            notification.timer.running = true;
            notification.timer.triggered.connect(function () {
                if (notification.id === undefined)
                    return;
                expirePopup(notification.id);
            });
        }
    }

    property list<Notification> current: []
    property var outputs

    function getOutput(target: string): ListModel {
        if (outputs === undefined)
            outputs = {};

        if (outputs[target] === undefined) {
            outputs[target] = Qt.createQmlObject("import QtQuick 2.0; ListModel {}", notifications);
        }

        return outputs[target];
    }

    function invokeAction(notificationId: int, actionId: string): void {
        const target = current.find(function (n) {
            return n ? n.id === notificationId : false;
        });
        if (!target)
            return;
        const action = target.actions.find(a => a.identifier === actionId);
        if (!action)
            return;
        action.invoke();
    }

    function expirePopup(notificationId: int): void {
        const target = current.find(n => n ? n.id === notificationId : false);
        if (!target)
            return;

        if (target.transient)
            target.expire();
        else {
            // Expiration should be cleaned up from the outputs, but not the history
            if (target.output === undefined) {
                return;
            }

            const output = target.output;
            output.append({
                "action": "remove",
                "target": notificationId
            });
        }
        target.isExpired = true;
    }

    function dismissAll(): void {
        while (current.length > 0) {
            if (current[0] == null)
                current.splice(0, 1);
            if (current[0].closedReason !== -1)
                continue;
            if (current[0].lastGeneration) {
                console.log(`Dismissing old: ${current[0].id}`);
                current.splice(0, 1);
            } else
                current[0].dismiss();
        }
    }

    function bindClose(notificationId: int, handler: var): void {
        const target = current.find(n => n ? n.id === notificationId : false);
        if (!target)
            return;

        target.closed.connect(handler);
    }
}
