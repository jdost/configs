import QtQuick
import Quickshell.Io

import qs
import qs.Common
import qs.Services

DetailsPopup {
    id: popup
    height: cores.height + processes.height + Config.em(0.5)
    width: Config.em(16)

    CircularBar {
        id: cpuBar

        color: {
            if (CpuUsage.usedPercent < 0.34)
                return U.rgba(0, 255, 0, 1.0)
            if (CpuUsage.usedPercent < 0.67)
                return U.rgba(255, 255, 0, 1.0)
            return U.rgba(255, 0, 0, 1.0)
        }
        size: Config.em(4)
        thickness: Config.em(0.5)
        value: CpuUsage.usedPercent
        y: Config.em(0.5)
        x: Config.em(0.2)

        Text {
            color: U.rgba(240, 240, 240, 1)
            font.pixelSize: Config.em(3)
            text: ""
            x: Config.em(1.2)
            y: -Config.em(0.2)
        }
    }

    Rectangle {
        id: cores

        color: "transparent"
        height: Config.em(1)
        width: popup.width - x
        x: cpuBar.width + cpuBar.thickness + Config.em(0.25)

        readonly property list<string> colors: [
            "#99f21584",
            "#997cf215",
            "#9915b7f2",
            "#99f21515",
            "#99eef215",
            "#991580f2",
            "#99f28b15",
            "#99be15f2"
        ];

        Repeater {
            model: CpuUsage.perCorePercent.length

            Rectangle {
                required property real index

                property real usage: CpuUsage.perCorePercent[index];

                anchors.bottom: cores.bottom
                color: cores.colors[index % cores.colors.length]
                height: Math.max(cores.height*usage, 2);
                width: cores.width/CpuUsage.perCorePercent.length;
                x: index*width;

                Behavior on height {
                    enabled: Config.animations
                    NumberAnimation {
                        duration: 200;
                    }
                }

                Behavior on y {
                    enabled: Config.animations
                    NumberAnimation {
                        duration: 200;
                    }
                }
            }
        }
    }

    Column {
        id: processes

        width: popup.width - x
        x: cores.x
        y: cores.height + Config.em(0.2)

        property list<var> procList: [];

        Repeater {
            model: 5

            Row {
                required property real index

                property string command: processes.procList.length > index ? processes.procList[index][2] : ""
                property string textColor: U.rgba(240, 240, 240, 1.0)
                property string pid: processes.procList.length > index ? processes.procList[index][1] : "0";
                property string usage: processes.procList.length > index ? processes.procList[index][0] : "0.0";

                spacing: 4
                width: processes.width

                Text {
                    id: usage

                    color: {
                        const parsed = Number(parent.usage)
                        if (parsed < 34)
                            return U.rgba(0, 255, 0, 0.8)
                        if (parsed < 67)
                            return U.rgba(255, 255, 0, 0.8)
                        return U.rgba(255, 0, 0, 0.8)
                    }
                    font.pixelSize: Config.em(0.8)
                    font.weight: 700
                    text: "%1%".arg(parent.usage)
                }
                Text {
                    anchors.baseline: usage.baseline
                    color: parent.textColor
                    font.pixelSize: Config.em(0.8)
                    text: parent.command
                }
                Text {
                    anchors.baseline: usage.baseline
                    color: U.rgba(200, 200, 200, 1)
                    font.pixelSize: Config.em(0.6)
                    text: "(%1)".arg(parent.pid)
                }
            }
        }

        Process {
            id: ps

            command: ["ps", "-o", "%cpu,pid,comm", "ax", "--sort=-%cpu", "--no-headers"]
            running: popup.shown

            stdout: StdioCollector {
                onStreamFinished: {
                    this.text.split("\n").slice(0, 6).map(function (line, index) {
                        return line.split(" ").filter((e) => e.length > 0);
                    }).filter((e) => e[2] !== "ps").slice(0, 5).forEach(function (result, index) {
                        if (index >= processes.procList) {
                            processes.procList.push(result);
                        } else {
                            processes.procList[index] = result
                        }
                    })
                }
            }
        }

        Timer {
            interval: 1000
            repeat: true
            running: popup.shown

            onTriggered: ps.running = popup.shown
        }
    }
}
