pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: brightnessService

    property real max: 1.0
    property real rawLevel: 1.0
    property real level: rawLevel / max

    Process {
        id: setupBacklight
        command: ['ls', '-w1', '/sys/class/backlight']
        running: true

        stdout: StdioCollector {
            onStreamFinished: {
                const target = this.text.trim();
                brightnessWatcher.path = `/sys/class/backlight/${target}/brightness`
                brightnessWatcher.watchChanges = true
                maxBrightnessWatcher.path = `/sys/class/backlight/${target}/max_brightness`
            }
        }
    }

    FileView {
        id: brightnessWatcher
        path: ""
        watchChanges: false

        onLoaded: {
            brightnessService.rawLevel = Number(this.text().trim());
        }

        onFileChanged: {
            this.reload();
            brightnessService.rawLevel = Number(this.text().trim());
        }
    }

    FileView {
        id: maxBrightnessWatcher
        path: ""
        watchChanges: false

        onLoaded: {
            brightnessService.max = Number(this.text().trim());
        }
    }
}
