import QtQuick
import qs
import qs.Services

Rectangle {
    id: root

    property var dateCells: ({})
    readonly property int day: 24 * 60 * 60 * 1000
    readonly property var monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "January"]
    property int month: {
        return (new Date()).getMonth();
    }
    property int year: {
        return (new Date()).getFullYear();
    }

    clip: true
    color: "transparent"
    implicitHeight: calendar.height + eventRow.height

    Component.onCompleted: {
        CalcurseService.lookupEvents(year, month);
    }

    Behavior on implicitHeight {
        enabled: Config.animations
        NumberAnimation {
            duration: 150
        }
    }

    Connections {
        target: CalcurseService

        function onEventsLoaded(events) {
            for (const d in events) {
                dateCells[d].events = events[d];
            }
        }
    }

    function getWeekStarts() {
        const first = new Date(year, month, 1);
        const end = new Date((month < 12 ? new Date(year, month + 1, 1) : new Date(year + 1, 1, 1)).valueOf() - day);
        const week = 7 * day;

        const beginning = new Date(first.valueOf() - (first.getDay() * day));
        var current = beginning;
        var sundays = [];
        while (current.valueOf() <= end) {
            sundays.push(current.valueOf());
            var currentRaw = new Date(current.valueOf() + week);
            // If this is a DST month, things get weird
            if (currentRaw.getHours() !== 0)
                currentRaw = new Date(currentRaw.valueOf() + 60 * 60 * 1000);
            current = new Date(currentRaw.getFullYear(), currentRaw.getMonth(), currentRaw.getDate());
        }
        return sundays;
    }
    Column {
        id: calendar

        readonly property int cellDim: Config.em(1.5)

        height: childrenRect.height
        width: 7 * cellDim
        x: (root.width - width) / 2

        Row {
            id: controls
            height: Config.em(0.9)

            Rectangle {
                property bool hovered: false

                color: hovered ? U.rgba(255, 255, 255, 0.3) : "transparent"
                height: controls.height
                radius: 10
                width: controls.height

                Text {
                    color: "white"
                    font.pixelSize: controls.height - 4
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: "<"
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        month = month - 1;
                        if (month === -1) {
                            month = 11;
                            year = year - 1;
                        }
                        CalcurseService.lookupEvents(year, month);
                        eventSummary.text = "";
                    }
                    onEntered: {
                        parent.hovered = true;
                    }
                    onExited: {
                        parent.hovered = false;
                    }
                }
            }

            Rectangle {
                color: "transparent"

                height: controls.height
                width: calendar.width - 2 * controls.height

                Text {
                    color: "white"
                    font.pixelSize: controls.height
                    horizontalAlignment: Text.AlignHCenter
                    text: monthNames[month]
                    width: parent.width
                }
            }

            Rectangle {
                property bool hovered: false

                color: hovered ? U.rgba(255, 255, 255, 0.3) : "transparent"
                height: controls.height
                radius: 10
                width: controls.height

                Text {
                    color: "white"
                    font.pixelSize: controls.height - 4
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: ">"
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        month = month + 1;
                        if (month === 12) {
                            month = 0;
                            year = year + 1;
                        }
                        CalcurseService.lookupEvents(year, month);
                        eventSummary.text = "";
                    }
                    onEntered: {
                        parent.hovered = true;
                    }
                    onExited: {
                        parent.hovered = false;
                    }
                }
            }
        }

        Repeater {
            id: repeater

            model: getWeekStarts()

            Row {
                id: week

                required property int index
                required property var modelData
                height: calendar.cellDim

                Repeater {
                    model: 7

                    Rectangle {
                        required property int index
                        property date current: {
                            new Date(week.modelData + (index * root.day) + 60 * 60 * 1000);
                        }
                        property var events: []

                        Component.onCompleted: {
                            root.dateCells[current.toDateString()] = this;
                        }

                        bottomLeftRadius: (index === 0 && (week.index + 1) === repeater.model.length) ? 15 : 0
                        bottomRightRadius: (index === 6 && (week.index + 1) === repeater.model.length) ? 15 : 0
                        color: {
                            if (current.getDay() === 0 || current.getDay() === 6)
                                return U.rgba(255, 255, 255, 0.1);
                            return "transparent";
                        }
                        height: calendar.cellDim
                        topLeftRadius: (index === 0 && week.index === 0) ? 15 : 0
                        topRightRadius: (index === 6 && week.index === 0) ? 15 : 0
                        width: calendar.cellDim

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: events.length > 0 ? Qt.PointingHandCursor : Qt.ArrowCursor
                            onClicked: {
                                eventSummary.text = events.map(function (e) {
                                    const d = new Date(e[0]);
                                    if (d.valueOf() < current.valueOf())
                                        return e[1];
                                    var clock = d.getHours() > 9 ? `${d.getHours()}` : `0${d.getHours()}`;
                                    clock += d.getMinutes() > 9 ? `:${d.getMinutes()}` : `:0${d.getMinutes()}`;
                                    if (clock === "00:00")
                                        return e[1];
                                    return `${clock} ${e[1]}`;
                                }).join("\n");
                            }
                        }

                        Text {
                            anchors.fill: parent
                            color: {
                                if (current.getMonth() !== root.month)
                                    return U.rgba(150, 150, 150, events.length > 0 ? 1 : 0.8);
                                return U.rgba(250, 250, 250, events.length > 0 ? 1 : 0.8);
                            }
                            font.bold: events.length > 0
                            font.pixelSize: Config.em(0.9)
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            text: {
                                return current.getDate();
                            }
                        }
                    }
                }
            }
        }
    }

    Rectangle {
        id: eventRow

        color: "transparent"
        height: visible ? eventSummary.height : 0
        width: root.width
        visible: eventSummary.text.length > 0
        x: Config.em(2)
        y: calendar.height

        Text {
            id: eventSummary
            color: "white"
            font.pixelSize: Config.em(1)
            text: ""
            width: root.width
        }
    }
}
