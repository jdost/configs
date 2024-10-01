import { GradientIcon } from "../widgets/icons.js";
import { add_icon } from "../widgets/bar.js";

const cpuUsage = Variable(0);
var lastReading = [-1, -1];
const cpuInterval = Utils.interval(1000, function () {
  Utils.readFileAsync("/proc/stat").then(function (content) {
    const cumulative = content.split("\n")[0].split(" ");
    const user = parseInt(cumulative[2], 10);
    const nice = parseInt(cumulative[3], 10);
    const system = parseInt(cumulative[4], 10);
    const idle = parseInt(cumulative[5], 10);
    const iowait = parseInt(cumulative[6], 10);
    const steal = parseInt(cumulative[9], 10);
    const usage = user + nice + system + iowait + steal;
    const total = usage + idle;

    if (lastReading[0] !== -1) {
      cpuUsage.value =
        ((usage - lastReading[0]) / (total - lastReading[1])) * 100;
    }
    lastReading = [usage, total];
  });
});

add_icon(
  Widget.EventBox({
    class_name: "cpu",
    child: GradientIcon("", "CPU", cpuUsage.bind()),
    on_primary_click: function (_) {
      console.log(cpuUsage.value);
    },
  }),
);
