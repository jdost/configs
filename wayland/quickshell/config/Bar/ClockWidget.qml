import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Io
import qs
import qs.Services
import qs.Sidebar

Rectangle {
    id: root

    property ShellScreen screen
    readonly property int minute: 1000 * 60

    color: {
        if (!CalcurseService.enabled)
            return "transparent";
        if (CalcurseService.nextAppointment === undefined)
            return "transparent";

        var timeUntil = CalcurseService.nextAppointment.valueOf() - (clock.date.valueOf());
        if (timeUntil > (20 * minute))
            return "transparent";
        if (timeUntil > (10 * minute))
            return U.rgba(255, 255, 0, 0.4);
        if (timeUntil > (5 * minute))
            return U.rgba(255, 153, 0, 0.4);
        if (timeUntil > 0)
            return U.rgba(255, 0, 0, 0.4);
        return U.rgba(85, 170, 255, 0.4);
    }
    implicitWidth: display.width + 12
    implicitHeight: display.height + Config.em(0.3)
    radius: 15
    y: parent.topPadding

    Text {
        id: display

        text: Qt.formatDateTime(clock.date, "hh:mm:ss")
        color: "#FFFFFF"
        font.family: "monospace"
        font.pixelSize: Config.em(0.7)
        x: 6
        y: Config.em(0.15)
    }

    MouseArea {
        id: mouse

        acceptedButtons: Qt.LeftButton | Qt.RightButton
        anchors.fill: parent
        hoverEnabled: true
        onClicked: mouse => {
            if (mouse.button === Qt.LeftButton)
                sidebar.toggle(root.screen);
            else if (mouse.button === Qt.RightButton) {
                if (!CalcurseService.enabled)
                    return;

                var timeUntil = CalcurseService.nextAppointment.valueOf() - (clock.date.valueOf());
                var body = "Started";
                if (timeUntil > (60 * 60 * 1000))
                    body = `Starts in ${Math.floor(timeUntil / (60 * 60 * 1000))} hours`;
                else if (timeUntil > (60 * 1000))
                    body = `Starts in ${Math.floor(timeUntil / (60 * 1000))} minutes`;
                else if (timeUntil > 0)
                    body = `Starts in ${Math.floor(timeUntil / 1000)} seconds`;

                reminder.exec(["notify-send", "--icon=calendar", "--transient", "--expire-time=5000", CalcurseService.nextAppointmentName, body]);
            }
        }
        onEntered: {
            tooltip.open();
        }
        onExited: {
            tooltip.close();
        }
    }

    // Notification "Process" that get's set via `exec`
    Process {
        id: reminder

        running: false
    }

    ToolTip {
        id: tooltip

        delay: 500
        padding: 4
        popupType: Popup.Native
        y: 1.5 * root.height

        contentItem: Text {
            text: Qt.formatDateTime(clock.date, "ddd MM/dd/yyyy")
            color: U.rgba(17, 17, 17, 1)
            font.pixelSize: Config.em(0.7)
        }

        background: Rectangle {
            radius: 15
            color: U.rgba(212, 212, 212, 0.65)
        }

        enter: Transition {
            enabled: Config.animations
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: 250
            }
        }

        exit: Transition {
            enabled: Config.animations
            NumberAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: 250
            }
        }
    }

    SystemClock {
        id: clock

        precision: SystemClock.Seconds
    }
}
