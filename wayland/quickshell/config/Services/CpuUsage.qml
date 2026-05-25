pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: cpu

    readonly property int interval: 1000

    property real total: 1
	property real used: 0
    property real usedPercent: 0

    property list<real> perCoreTotal: [];
    property list<real> perCoreUsed: [];
    property list<real> perCorePercent: [];

	Timer {
	    interval: cpu.interval
        running: true
        repeat: true

	    onTriggered: {
            stat.reload();
            const rawStats = stat.text().split("\n");

            function calcUsage(line) {
                const stats = line.split(" ")
                const baseIndex = stats[0] === "cpu" ? 2 : 1;
                const user = Number(stats[baseIndex]);
                const nice = Number(stats[baseIndex + 1]);
                const system = Number(stats[baseIndex + 2]);
                const idle = Number(stats[baseIndex + 3]);
                const iowait = Number(stats[baseIndex + 4]);
                const steal = Number(stats[baseIndex + 7]);

                const usedSum = user + nice + system + iowait + steal;
                const totalSum = usedSum + idle;
                return [usedSum, totalSum]
            }

            var calcValues = calcUsage(rawStats[0])
            const fullUsed = calcValues[0];
            const fullTotal = calcValues[1];
            const prevUsed = used
            const prevTotal = total

            usedPercent = (fullUsed - prevUsed) / (fullTotal - prevTotal)
            used = fullUsed
            total = fullTotal

            var line = 1;
            while (rawStats[line].startsWith("cpu")) {
                const core = line - 1;
                if (core >= perCoreTotal.length) {
                    perCoreTotal[core] = 1;
                    perCoreUsed[core] = 0;
                    perCorePercent[core] = 0.0;
                }
                var calcValues = calcUsage(rawStats[line]);
                const coreUsed = calcValues[0]
                const coreTotal = calcValues[1]
                const prevUsed = perCoreUsed[core]
                const prevTotal = perCoreTotal[core]

                perCorePercent[core] = (coreUsed - prevUsed) / (coreTotal - prevTotal);
                perCoreUsed[core] = coreUsed
                perCoreTotal[core] = coreTotal

                line++;
            }
        }
	}

	FileView { id: stat; path: "/proc/stat" }
}
