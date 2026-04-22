pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Hyprland
import Quickshell.Services.Notifications

Singleton {
    id: notifications

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

        onNotification: function(notification) {
            notification.tracked = true;
            current.push(notification)
            if (notification.isExpired || notification.lastGeneration)
                return;

            const output = getOutput(Hyprland.focusedMonitor.name)
            output.append({"msg": notification});
        }
    }

    property list<Notification> current: [];
    property var outputs;

    function getOutput(target: string): ListModel {
        if (outputs === undefined)
            outputs = {};

        if (outputs[target] === undefined) {
            const listModel = Qt.createComponent("QtQml.Models", "ListModel");
            outputs[target] = listModel.createObject(notifications);
        }

        return outputs[target];
    }

    function invokeAction(notificationId: int, actionId: string): void {
        const target = current.find((n) => n.id === notificationId)
        if (!target)
            return;
        const action = target.actions.find((a) => a.identifier === actionId)
        if (!action)
            return;
        action.invoke();
    }

    function expirePopup(notificationId: int): void {
        const target = current.find((n) => n.id === notificationId)
        if (!target)
            return;
        target.expire();
        target.isExpired = True;
    }
}
