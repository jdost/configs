import qs
import qs.Services

Icon {
    icon: ""
    iconColor: U.gradientColor(CpuUsage.usedPercent)
    module: "cpu"
    size: Config.em(1.4)
    tooltip: `CPU: ${(CpuUsage.usedPercent * 100).toFixed(2)}%`
    topPadding: Config.em(0.05)
}
