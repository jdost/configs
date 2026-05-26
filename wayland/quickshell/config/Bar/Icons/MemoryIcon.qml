import qs
import qs.Services
import qs.Popups

Icon {
    icon: ""
    iconColor: U.gradientColor(MemoryUsage.usedPercent)
    module: "memory"
    size: Config.em(1.4)
    tooltip: `Memory: ${(MemoryUsage.usedPercent * 100).toFixed(2)}%`
    topPadding: Config.em(0.05)

    onClicked: function () {
        popup.toggle();
    }

    MemoryPopup {
        id: popup
    }
}
