import qs
import qs.Services
import qs.Popups

Icon {
    icon: ""
    iconColor: U.gradientColor(CpuUsage.usedPercent)
    module: "cpu"
    size: Config.em(1.4)
    tooltipEnabled: !popup.shown
    tooltip: `CPU: ${(CpuUsage.usedPercent * 100).toFixed(2)}%`
    topPadding: Config.em(0.05)
    onClicked: function () {
        popup.toggle();
    }

    CpuPopup {
        id: popup
    }
}
