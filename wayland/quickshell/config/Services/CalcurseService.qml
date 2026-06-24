pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: root

    property bool enabled: true

    readonly property string prefix: "**"
    readonly property string delimiter: "\r"
    readonly property string format: `${prefix}%s${delimiter}%d${delimiter}%m\n`
    readonly property int day: 1000 * 60 * 60 * 24
    readonly property int maxDate: day * 1000000000
    readonly property int postEventWindow: 1000 * 60 * 5
    readonly property int reminderWindow: 1000 * 60 * 2

    property date nextAppointment
    property string nextAppointmentName: "Unset"

    Process {
        id: calcurseNext
        command: ["calcurse", "-Q", "--filter-type", "cal", "--day", "7", `--format-apt=${format}`, `--format-recur-apt=${format}`]
        running: false

        stdout: StdioCollector {
            onStreamFinished: {
                const now = new Date();
                var appointments = this.text.split("\n").map(function (line) {
                    if (!line.startsWith(prefix))
                        return undefined;

                    const start = new Date(Number(line.split(delimiter, 1)[0].substr(prefix.length)) * 1000);
                    const duration = Number(line.split(delimiter, 2)[1]) * 1000;
                    // Skip day long events
                    if (duration > day)
                        return undefined;
                    const event = line.split(delimiter, 3)[2];

                    return {
                        start: start,
                        name: event
                    };
                }).filter(i => i != undefined).filter(function (e) {
                    return (e.start.valueOf() + postEventWindow) > now.valueOf();
                });

                if (appointments.length == 0) {
                    nextAppointment = new Date(maxDate);
                    // If no appointment in the window, check again in a day
                    updateNext.interval = day;
                    updateNext.restart();
                    return;
                }
                nextAppointment = appointments[0].start;
                nextAppointmentName = appointments[0].name;
                // Update nextAppointment after this one occurs + window
                updateNext.interval = nextAppointment.valueOf() - now.valueOf() + postEventWindow;
                updateNext.restart();
                // Popup a reminder
                const reminderTime = nextAppointment.valueOf() - now.valueOf() - reminderWindow;
                if (reminderTime > 0) {
                    reminderPopup.interval = reminderTime;
                    reminderPopup.restart();
                }
            }
        }
    }
    // Scheduled timer for when the next appointment has cleared to update
    Timer {
        id: updateNext

        interval: maxDate
        running: false
        repeat: false

        onTriggered: calcurseNext.running = true
    }
    // Process to generate the reminder popup
    Process {
        id: reminder

        running: false
    }
    // Scheduled timer for a reminder popup
    Timer {
        id: reminderPopup

        interval: maxDate
        running: false
        repeat: false

        onTriggered: {
            reminder.exec(["notify-send", "--icon=calendar", "--transient", "--expire-time=15000", nextAppointmentName, "Starts in 2 minutes"]);
        }
    }
    // This is to get inotify events for lazy updates
    FileView {
        id: calcurseFile
        path: `${Quickshell.env("HOME")}/.local/share/calcurse/apts`
        printErrors: false
        watchChanges: true

        onFileChanged: calcurseNext.running = true
        onLoaded: calcurseNext.running = true
        onLoadFailed: function (e) {
            // Assume if the load failed, calcurse isn't supported
            enabled = false;
        }
    }
}
