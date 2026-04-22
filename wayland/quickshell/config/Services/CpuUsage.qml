pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: cpu

    readonly property int interval: 1000

    property real total: 1
	property real used: 0
    property real usedPercent: used / total

    property real previousTotal: 1
    property real previousUsed: 0


	Timer {
	    interval: cpu.interval
        running: true
        repeat: true

	    onTriggered: {
            stat.reload();
            const rawStat = stat.text();

            const stats = rawStat.split("\n")[0].split(" ");
            const user = Number(stats[2]);
            const nice = Number(stats[3]);
            const system = Number(stats[4]);
            const idle = Number(stats[5]);
            const iowait = Number(stats[6]);
            const steal = Number(stats[9]);

            const fullUsed = user + nice + system + iowait + steal;
            const fullTotal = fullUsed + idle;

            used = fullUsed - previousUsed;
            total = fullTotal - previousTotal;
            previousUsed = fullUsed;
            previousTotal = fullTotal;
        }
	}

	FileView { id: stat; path: "/proc/stat" }
}
