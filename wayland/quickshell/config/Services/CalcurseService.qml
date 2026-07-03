pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: root

    property bool enabled: true

    readonly property string prefix: "**"
    readonly property string delimiter: "\r"
    readonly property string format: `${prefix}%s${delimiter}%d${delimiter}%S${delimiter}%m\n`
    readonly property int day: 1000 * 60 * 60 * 24
    readonly property var maxDate: (new Date(2100, 1, 1)).valueOf()
    readonly property int postEventWindow: 1000 * 60 * 5
    readonly property int reminderWindow: 1000 * 60 * 2

    property date nextAppointment
    property string nextAppointmentName: "Unset"

    signal eventsLoaded(events: var)

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
                    const event = line.split(delimiter, 4)[3];

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

    function formatDate(d): str {
        const month = d.getMonth() < 9 ? `0${d.getMonth() + 1}` : `${d.getMonth() + 1}`;
        const date = d.getDate() < 10 ? `0${d.getDate()}` : `${d.getDate()}`;
        return `${month}/${date}/${d.getFullYear()}`;
    }

    function lookupEvents(year, month) {
        const first = new Date(year, month, 1);
        const last = new Date((month < 12 ? new Date(year, month + 1, 1) : new Date(year + 1, 1, 1)).valueOf() - day);
        const start = new Date(first.valueOf() - first.getDay() * day);
        const end = new Date(last.valueOf() + (6 - last.getDay()) * day);
        calcurseEvents.exec(["calcurse", "-Q", "--filter-type", "apt", "--from", formatDate(start), "--to", formatDate(end), `--format-apt=${format}`]);
    }
    function getEvents(d) {
        if (events[d.toDateString()] === undefined)
            events[d.toDateString()] = [];
        return events[d.toDateString()];
    }
    Process {
        id: calcurseEvents

        running: false
        stdout: StdioCollector {
            onStreamFinished: {
                var events = {};
                this.text.split("\n").map(function (line) {
                    if (!line.startsWith(prefix))
                        return undefined;

                    const start = new Date(Number(line.split(delimiter, 1)[0].substr(prefix.length)) * 1000);
                    const duration = Number(line.split(delimiter, 2)[1]) * 1000;
                    const startTime = line.split(delimiter)[2];
                    if (startTime === "..:..")
                        return undefined;
                    const event = line.split(delimiter)[3];

                    return {
                        start: start,
                        duration: duration,
                        name: event
                    };
                }).filter(i => i != undefined).forEach(function (d) {
                    var remaining = d.duration;
                    var date = d.start;
                    while (remaining > 0) {
                        if (events[date.toDateString()] === undefined) {
                            events[date.toDateString()] = [];
                        }
                        events[date.toDateString()].push([d.start.valueOf(), d.name]);
                        remaining = remaining - day;
                        date = new Date(date.valueOf() + day);
                    }
                });
                eventsLoaded(events);
            }
        }
    }
}
