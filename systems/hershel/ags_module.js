import { set_monitor, get_monitor } from "../widgets/notifications.js";
import { addToggle } from "../widgets/sidebar.js";

const monitor = Variable(0);

addToggle({
  icon: monitor.bind().as(function (m) {
    return m === 0 ? "󱂫" : "󱂪";
  }),
  tooltip: "Switch notification monitor",
  get_state: function () {
    const resolved_monitor = get_monitor();
    monitor.value = resolved_monitor > -1 ? resolved_monitor : 0;
    return monitor.value === 1;
  },
  set_state: function (s) {
    if (s) {
      // setting to true is monitor 1
      set_monitor(1);
      monitor.value = 1;
    } else {
      set_monitor(0);
      monitor.value = 0;
    }
  },
});
