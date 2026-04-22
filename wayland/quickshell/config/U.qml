pragma Singleton
import QtQuick
import Quickshell

Singleton {
    id: utils

    function rgba(r: int, g: int, b: int, a: real): color {
        return Qt.rgba(r/255, g/255, b/255, a);
    }

    function rgb(r: int, g: int, b: int): color {
        return Qt.rgba(r/255, g/255, b/255, 1.0);
    }


    function gradientColor(val: real): color {
        var low = rgba(255, 255, 0, 1.0);
        var high = rgba(255, 0, 0, 1.0);

        if (val < 0.5) {
            low = rgba(0, 255, 0, 1.0);
            high = rgba(255, 255, 0, 1.0);
            val = val * 2;
        } else {
            val = val * 2 - 1;
        }
        return Qt.rgba(
            low.r + ((high.r - low.r) * val),
            low.g + ((high.g - low.g) * val),
            low.b + ((high.b - low.b) * val),
            1.0
        )
    }
}
