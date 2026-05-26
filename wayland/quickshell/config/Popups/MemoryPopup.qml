import QtQuick
import QtQuick.Shapes
import Quickshell.Io

import qs
import qs.Common
import qs.Services

DetailsPopup {
    id: popup
    height: info.height + processes.height + Config.em(0.5)
    width: Config.em(16)

    readonly property string bufferedColor: U.rgba(255, 200, 0, 1)
    readonly property string cachedColor: U.rgba(0, 255, 255, 1)
    readonly property string slabColor: U.rgba(200, 0, 255, 1)
    readonly property string usedColor: U.rgba(0, 255, 0, 1)

    function humanReadable(kb): string {
        const units = ["KB", "MB", "GB", "TB"]
        var i = 0

        var output = kb
        while (output > 1024) {
            output = output / 1024
            i++;
        }

        return `${output.toFixed(2)} ${units[i]}`;
    }

    CircularBar {
        id: memoryBar

        color: usedColor
        size: Config.em(4)
        thickness: Config.em(0.5)
        value: MemoryUsage.usedPercent
        y: Config.em(0.5)
        x: Config.em(0.2)

        Text {
            color: U.rgba(240, 240, 240, 1)
            font.pixelSize: Config.em(3)
            text: ""
            x: Config.em(1.2)
            y: -Config.em(0.2)
        }

        SubSegment {
            color: slabColor
            offset: MemoryUsage.used
            value: MemoryUsage.slabCached
        }

        SubSegment {
            capStyle: ShapePath.RoundCap
            color: bufferedColor
            offset: MemoryUsage.used + MemoryUsage.slabCached + MemoryUsage.pageCache
            value: MemoryUsage.buffered
        }

        SubSegment {
            color: cachedColor
            offset: MemoryUsage.used + MemoryUsage.slabCached
            value: MemoryUsage.pageCache
        }
    }

    Rectangle {
        id: info

        color: "transparent"
        height: Config.em(1.8)
        width: popup.width - x
        x: memoryBar.width + memoryBar.thickness + Config.em(0.25)

        Rectangle {
            color: "transparent"
            height: Config.em(0.5)
            x: 0

            Text {
                color: slabColor
                font.pixelSize: Config.em(0.5)
                text: `SysCache: ${humanReadable(MemoryUsage.slabCached)}`
            }
        }

        Rectangle {
            color: "transparent"
            height: Config.em(0.5)
            x: 0
            y: Config.em(0.6)

            Text {
                color: cachedColor
                font.pixelSize: Config.em(0.5)
                text: `PageCache: ${humanReadable(MemoryUsage.pageCache)}`
            }
        }

        Rectangle {
            color: "transparent"
            height: Config.em(0.5)
            width: Config.em(3)
            x: 0
            y: Config.em(1.2)

            Text {
                color: bufferedColor
                font.pixelSize: Config.em(0.5)
                text: `Buffers: ${humanReadable(MemoryUsage.buffered)}`
            }
        }

        Rectangle {
            color: "transparent"
            height: Config.em(1.8)
            x: Config.em(6)

            Rectangle {
                id: swapBar

                color: U.rgba(66, 66, 66, 1.0)
                height: Config.em(0.8)
                radius: 10
                width: info.width - parent.x
                y: Config.em(0.8)

                Rectangle {
                    id: swapCacheBar

                    bottomLeftRadius: 10
                    color: cachedColor
                    height: swapBar.height - 4
                    topLeftRadius: 10
                    width: (swapBar.width - 4) * (MemoryUsage.swapCached/MemoryUsage.swapTotal)
                    x: 2
                    y: 2
                }

                Rectangle {
                    bottomRightRadius: 10
                    color: usedColor
                    topRightRadius: 10
                    width: (swapBar.width - 4) * ((MemoryUsage.swapTotal - MemoryUsage.swapFree) / MemoryUsage.swapTotal)
                    y: 2
                    x: swapCacheBar.width + 2
                }
            }

            Text {
                color: U.rgba(240, 240, 240, 1)
                font.pixelSize: Config.em(0.5)
                horizontalAlignment: Text.AlignRight
                text: "Swap"
                x: Config.em(3.5)
                y: Config.em(0.8)
            }
        }

    }

    Column {
        id: processes

        width: popup.width - x
        x: info.x
        y: info.height + Config.em(0.2)

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

            command: ["ps", "-o", "%mem,pid,comm", "ax", "--sort=-%mem", "--no-headers"]
            running: popup.shown

            stdout: StdioCollector {
                onStreamFinished: {
                    this.text.split("\n").slice(0, 5).forEach(function (line, index) {
                        const result = line.split(" ").filter((e) => e.length > 0);
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

    component SubSegment: ShapePath {
        required property string color
        required property real offset
        required property real value

        fillColor: "transparent"
        strokeColor: color
        strokeStyle: ShapePath.SolidLine
        strokeWidth: memoryBar.thickness

        PathAngleArc {
            centerX: memoryBar.size / 2
            centerY: memoryBar.size / 2
            radiusX: memoryBar.size / 2
            radiusY: memoryBar.size / 2
            startAngle: {
                return memoryBar.startPosition + (offset / MemoryUsage.total * 360 * memoryBar.direction)
            }
            sweepAngle: value / MemoryUsage.total * 360 * memoryBar.direction
        }

    }

}
