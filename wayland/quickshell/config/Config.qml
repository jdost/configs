pragma Singleton
import QtQml
import Quickshell
import Quickshell.Io

Singleton {
    id: root
    readonly property string path: Qt.resolvedUrl("./settings.json")

    property list<string> modules: []
    property int scale: 24
    property string primaryMonitor

    function enabled(target: string) : bool {
        return modules.indexOf(target) != -1;
    }

    function em(x: real) : real {
        return (x * scale);
    }

    Component.onCompleted: {
        loadSettings();
    }

    FileView {
        id: settingsFile
        path: root.path
        blockLoading: true
    }

    function loadSettings() {
        var loadedSettings = {
            modules: ["clock"]
        };

        try {
            loadedSettings = JSON.parse(settingsFile.text());
        } catch (e) {
            console.log("Error loading settings:", e);
        }

        if (loadedSettings === null) {
            return;
        }

        if (loadedSettings.modules !== undefined)
            root.modules = loadedSettings.modules;
        root.primaryMonitor = loadedSettings.primaryMonitor
        if (loadedSettings.scale !== undefined)
            root.scale = loadedSettings.scale
    }
}
