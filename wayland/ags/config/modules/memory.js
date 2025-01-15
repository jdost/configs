import { GradientIcon } from "../widgets/icons.js";
import { addIcon } from "../widgets/bar.js";

const memoryUsage = Variable(0);
const memoryInterval = Utils.interval(1000, function () {
  Utils.readFileAsync("/proc/meminfo").then(function (content) {
    var total = -1;
    var free = -1;

    const lines = content.split("\n");
    for (var i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (!line.includes(":")) {
        continue;
      }
      var vals = line.split(":");
      const v = vals[1].trim();
      const k = vals[0].trim();
      if (k === "MemTotal") total = parseInt(v.split(" ")[0], 10);
      if (k == "MemFree") free = parseInt(v.split(" ")[0], 10);
    }

    memoryUsage.value = ((total - free) / total) * 100;
  });
});

addIcon(
  Widget.EventBox({
    class_name: "memory",
    child: GradientIcon("", "Memory", memoryUsage.bind()),
    on_primary_click: function (_) {
      console.log(`Memory: ${memoryUsage.value}`);
    },
  }),
);
