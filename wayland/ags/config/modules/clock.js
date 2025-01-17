import calcurse from "../services/calcurse.js";
import { addRight } from "../widgets/bar.js";
import Calendar from "../widgets/calendar.js";
import { toggle as sidebarToggle, addBlock } from "../widgets/sidebar.js";
import settings from "../settings.js";
import { YELLOW, ORANGE, RED, CYAN, WHITE } from "../widgets/color.js";
import GLib from "gi://GLib";

const time = Variable("", {
  poll: [1000, 'date "+%H:%M:%S"'],
});
const date = Variable("", {
  poll: [60 * 1000, 'date "+%A, %x"'],
});

const MINUTE = 1000 * 60;
const DAY = 24 * 60 * MINUTE;
const NOTIFY_BEFORE_SECS = 2 * 60;
const DEFAULT_REMINDER_TIMEOUT = 15;
const appointment_cutoffs = [
  [20 * MINUTE, YELLOW],
  [10 * MINUTE, ORANGE],
  [5 * MINUTE, RED],
  [0, CYAN],
  [-5 * MINUTE, undefined],
];
calcurse.postAppointmentHoldSecs = 5 * 60;
// How long to wait to get the next appointment after the current starts

function get_color(time_until) {
  var color = undefined;
  for (const i in appointment_cutoffs) {
    if (appointment_cutoffs[i][0] < time_until) break;
    color = appointment_cutoffs[i][1];
  }
  return color;
}

function zfill(n) {
  if (n < 10) {
    return `0${n}`;
  }
  return `${n}`;
}

function timePP(time_msec) {
  const time = new Date(time_msec);
  return `${zfill(time.getHours())}:${zfill(time.getMinutes())}`;
}

function datePP(time_msec) {
  const time = new Date(time_msec);
  return `${zfill(time.getMonth())}/${zfill(time.getDate())}/${time.getFullYear()}`;
}

function durationPP(duration) {
  const m = Math.floor(duration / MINUTE);
  const s = Math.floor(duration / 1000 - m * 60);

  return m > 0 ? `${m}m${s}s` : `${s}s`;
}

const reminder = (function () {
  var notification = undefined;

  function show(timeout_) {
    if (calcurse.next_appointment === calcurse.MAX_DATE) return;

    const timeout = timeout_ || DEFAULT_REMINDER_TIMEOUT * 1000;
    var body = "";
    if (calcurse.msecUntilNext() > DAY)
      body = `Starts on ${datePP(calcurse.next_appointment)}`;
    else if (calcurse.msecUntilNext() > 30 * MINUTE)
      body = `Starts at ${timePP(calcurse.next_appointment)}`;
    else body = `Starts in ${durationPP(calcurse.msecUntilNext())}`;

    notification = Utils.notify({
      summary: calcurse.nextAppointmentSummary(),
      body: calcurse.msecUntilNext() > 0 ? body : "Started",
      iconName: "calendar",
      transient: true,
      timeout: timeout,
    });
  }

  var autoTriggered = false;
  const interval = setInterval(function () {
    const msecUntil = calcurse.msecUntilNext();
    if (msecUntil < 0) return;
    if (msecUntil < NOTIFY_BEFORE_SECS * 1000 && !autoTriggered) {
      console.log(
        `Auto Notification for: ${calcurse.nextAppointmentSummary()}`,
      );
      show(DEFAULT_REMINDER_TIMEOUT * 1000);
      autoTriggered = true;
    } else if (msecUntil > NOTIFY_BEFORE_SECS * 1000 && autoTriggered) {
      autoTriggered = false;
    }
  }, 5 * 1000);

  return show;
})();

addRight(
  Widget.EventBox({
    child: Widget.Label({
      class_name: "clock",
      label: time.bind(),
      css: calcurse
        .nextCountdown(5)
        .bind()
        .as(function (msec_until) {
          const color = get_color(msec_until);
          if (color) return `background-color: ${color.with_alpha(0.4)};`;
          return "background-color: transparent;";
        }),
      tooltip_text: date.bind(),
    }),
    on_primary_click: function (_, e) {
      if (settings.sidebarEnabled) sidebarToggle();
    },
    on_secondary_click: function () {
      reminder(5 * 1000);
    },
  }),
  false,
);

addBlock(function () {
  const details = Widget.Label({
    class_name: "details",
    maxWidthChars: 70,
    truncate: "end",
  });
  // There's a small rendering bug, the visible flag isn't honored on render,
  // probably because it's draw related, so set it after a small timeout to happen
  // after any draw event to make it consistent
  setTimeout(function () {
    details.visible = false;
  }, 25);

  const now = new Date();
  const cal = Calendar({
    on_select: function (date) {
      details.label = calcurse
        .getAppointments()
        .filter(function (apt) {
          return (
            apt.start.getFullYear() === date.getFullYear() &&
            apt.start.getMonth() === date.getMonth() &&
            apt.start.getDate() === date.getDate()
          );
        })
        .map(function (apt) {
          return `${timePP(apt.start.valueOf())} - ${apt.summary}`;
        })
        .join("\n");
      details.visible = details.label.length !== 0;
    },
  });
  calcurse.getAppointments().forEach(function (appointment) {
    const time = appointment.start;
    if (time.getMonth() === now.getMonth()) cal.mark_day(time.getDate());
  });

  return Widget.Box({
    class_name: "calendar-holder",
    vertical: true,
    children: [
      Widget.CenterBox({
        vertical: false,
        centerWidget: Widget.Box({
          vertical: true,
          homogeneous: false,
          children: [cal],
        }),
      }),
      details,
    ],
  });
});
