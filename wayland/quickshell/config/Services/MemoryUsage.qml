pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: memory

    readonly property int interval: 1000

    property real total: 1
	property real free: 1024*1024*1024*1024
	property real used: total - free
    property real usedPercent: used / total


	Timer {
	    interval: memory.interval
        running: true
        repeat: true

	    onTriggered: {
            meminfo.reload()
            const rawMemInfo = meminfo.text()

            total = Number(rawMemInfo.match(/MemTotal: *(\d+)/)?.[1] ?? 1)
            free = Number(rawMemInfo.match(/MemFree: *(\d+)/)?.[1] ?? 0)
        }
	}

	FileView { id: meminfo; path: "/proc/meminfo" }
}
