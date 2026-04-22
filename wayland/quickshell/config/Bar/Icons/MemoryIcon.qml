import qs
import qs.Services


Icon {
    icon: ""
    iconColor: U.gradientColor(MemoryUsage.usedPercent)
    module: "memory"
    size: Config.em(1.4)
    tooltip: `Memory: ${(MemoryUsage.usedPercent * 100).toFixed(2)}%`
}
