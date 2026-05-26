pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: memory

    readonly property int interval: 1000

    property real available: 1024*1024*1024*1024
    property real buffered: 0
    property real cached: 0
	property real free: 1024*1024*1024*1024
    property real locked: 0
    property real pageCache: cached - shmem
    property real shmem: 0
    property real slabCached: 0
    property real slabLocked: 0
    property real slabTotal: 0
    property real swapCached: 0
    property real swapFree: 1
    property real swapTotal: 1
    property real total: 1
	property real used: total - available
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
            available = Number(rawMemInfo.match(/MemAvailable: *(\d+)/)?.[1] ?? 0)
            buffered = Number(rawMemInfo.match(/Buffers: *(\d+)/)?.[1] ?? 0)
            cached = Number(rawMemInfo.match(/Cached: *(\d+)/)?.[1] ?? 0)
            swapCached = Number(rawMemInfo.match(/SwapCached: *(\d+)/)?.[1] ?? 0)
            locked = Number(rawMemInfo.match(/Unevictable: *(\d+)/)?.[1] ?? 0)
            swapTotal = Number(rawMemInfo.match(/SwapTotal: *(\d+)/)?.[1] ?? 1)
            swapFree = Number(rawMemInfo.match(/SwapFree: *(\d+)/)?.[1] ?? 0)
            shmem = Number(rawMemInfo.match(/Shmem: *(\d+)/)?.[1] ?? 0)
            slabTotal = Number(rawMemInfo.match(/Slab: *(\d+)/)?.[1] ?? 0)
            slabCached = Number(rawMemInfo.match(/SReclaimable: *(\d+)/)?.[1] ?? 0)
            slabLocked = Number(rawMemInfo.match(/SUnreclaim: *(\d+)/)?.[1] ?? 0)
        }
	}

	FileView { id: meminfo; path: "/proc/meminfo" }
}
