const DAY = 1000 * 60 * 60 * 24;

function buildDay(day, opts) {
  const today = new Date();
  const widget = Widget.Button({
    attribute: day.valueOf(),
    child: Widget.Label(
      day.getDate() < 10 ? `0${day.getDate()}` : `${day.getDate()}`,
    ),
    tooltip_text: day.toDateString(),
    ...(opts || {}),
  });

  // Add day specific classes for style control
  if (day.getMonth() !== today.getMonth())
    widget.toggleClassName("off-month", true);

  if (day.getDay() === 0 || day.getDay() === 6)
    widget.toggleClassName("weekend", true);

  if (day.getMonth() === today.getMonth() && day.getDate() === today.getDate())
    widget.toggleClassName("today", true);

  return widget;
}

export default function Calendar(opts_) {
  /**
   * Calendar Widget -- The GTK provided one doesn't allow styling (or at least
   * in an obvious way), so just provide what we want.  This provides a Box with
   * sub boxes for each week (class is week), then buttons for each day.  These
   * buttons get classes for other months (i.e. days before/after first and last of
   * the month), weekends, today, and marked.  There is a provided method for
   * marking a day (like showing an event scheduled).  All buttons, on click, run
   * the passed in `on_select` method, with the Date for that button.
   **/
  const opts = {
    ...opts_,
  };
  // Calculate some basic date math, take today, move to first of the current month
  const today = new Date();
  const first = new Date(today.getFullYear(), today.getMonth(), 1);
  // Define iterator start as the first day of the week that contains the first day
  // of the current month (so it is the first cell on the first week)
  var day = new Date(first.valueOf() - DAY * first.getDay());
  // Rows are each filled out week, then `row` is the currently week being populated
  var rows = [];
  var row = undefined;
  // Day_lookup is just a reference for the day of the current month and the
  // corresponding widget, we use this in the `mark_day` method for adding to days
  // that have something like an event on them
  var day_lookup = {};

  while (true) {
    // Start a new row if it's the first of the week
    if (day.getDay() === 0) row = [];
    const widget = buildDay(day, {
      onClicked: function (_) {
        const date = new Date(this.attribute);
        if (opts.on_select) opts.on_select(date);
      },
    });
    // Store this day widget in the lookup for marking purposes
    if (day.getMonth() === today.getMonth()) day_lookup[day.getDate()] = widget;
    row.push(widget);
    // If it's the end of the week, push the row into the calendar
    if (day.getDay() === 6) {
      rows.push(
        Widget.Box({
          class_name: "week",
          homogeneous: true,
          hexpand: true,
          children: row,
        }),
      );
    }
    // Stop iterating if it's the end of the week for the next month
    if (day.getDay() === 6 && day.getMonth() !== today.getMonth()) break;
    day = new Date(day.valueOf() + DAY);
  }

  const calendar = Widget.Box({
    class_name: "calendar",
    vertical: true,
    children: rows,
  });

  // The `mark_day` method is just used by the calendar definition to mark days as
  // significant, like they have an event on them.
  calendar.mark_day = function (day) {
    if (day_lookup[day]) {
      day_lookup[day].toggleClassName("marked", true);
      day_lookup[day].cursor = "pointer";
    }
  };

  return calendar;
}
