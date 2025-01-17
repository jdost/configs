import GLib from "gi://GLib";

const HOUR = 1000 * 60 * 60;
const DAY = 24 * HOUR;
const MAX_DATE_VAL = 100000000 * DAY;
// These are used for calcurse query parsing, the PREFIX is used to simplify marking
// appointments vs calcurse's built in headers and spacing and the query format
// is just the expected output for lines we will parse
const PREFIX = "**";
// Calcurse formatting:
//   PREFIX is just used as a marker for the lines to parse
//   %s is the seconds since epoch for the event's start, we then use this to
//      directly generate a Date() for richer control/logic
//   %m is the summary/title for the event
const QUERY_FORMAT = `${PREFIX}%s %m\n`;

class CalcurseService extends Service {
  /**
   * CalcurseService - A service for reactively generating data around appointments
   * from calcurse.  This won't be enabled (it just no-ops everything with minimal
   * overhead) if there is no appointments file at the designated location.  This
   * mostly monitors calcurse for new appointments and presents both all appointments
   * in the current month (for calendar display) and the next appointment on the
   * calendar.
   **/
  static {
    Service.register(
      this,
      {
        // Both the property and event give uint, which is just the underlying
        // `valueOf` for the Date type, can then be re-built with `new Date(v)`
        "new-appointment": ["uint64"],
      },
      {
        "next-appointment": ["uint64", "r"],
      },
    );
  }

  #next = {
    start: new Date(MAX_DATE_VAL),
    summary: "Nothing",
  };
  #appointments = [];
  #countdowns = []; // Collection of custom variable bindings for countdowns to the next appointment
  #nextRefresh = undefined;
  postAppointmentHoldSec = 60 * 10; // Setting for how long an appointment remains "next" after it starts

  get next_appointment() {
    return this.#next.start.valueOf();
  }

  constructor() {
    super();

    // Lookup where home is
    const home = Utils.exec('bash -c "echo $HOME"');
    this.APT_FILE = `${home}/.local/share/calcurse/apts`;
    this.MAX_DATE = new Date(MAX_DATE_VAL).valueOf(); // Give comparison ref for placeholder
    // If the apts file doesn't exist, mark everything as disabled
    if (this.APT_FILE !== Utils.exec(`ls ${this.APT_FILE}`)) {
      console.log("Calcurse not available, disabling...");
      this.enabled = false;
      return;
    }
    this.enabled = true;

    const self = this;
    // `refresh` is the method that updates the list of appointments and the next
    //   appointment trackers, we call this on build, whenever the apts file changes
    //   (i.e. an appointment was added/removed/changed), and then on an hour timer
    //   just to be defensive in case the file monitor misses
    Utils.monitorFile(this.APT_FILE, function () {
      self.refresh();
    });
    setInterval(function () {
      self.refresh();
    }, HOUR); // Hard check every hour
    this.refresh();
  }

  msecUntilNext() {
    // Helper method for providing the msec countdown value
    return this.next_appointment - new Date().valueOf();
  }

  nextCountdown(frequency) {
    // Generates a variable binding for reactivity based
    // on the msec until the next appointment, meant to simplify logic for things
    // like alerts around upcoming events
    if (!this.enabled) return Variable(MAX_DATE_VAL);

    const appointmentCountdown = Variable(MAX_DATE_VAL);
    this.#countdowns.push(appointmentCountdown);
    const self = this;
    const nextCountdown = setInterval(function () {
      appointmentCountdown.value = self.msecUntilNext();
    }, frequency * 1000);
    return appointmentCountdown;
  }

  _clearNextRefresh() {
    // next appointment lookup cleaner
    if (this.#nextRefresh !== undefined) {
      GLib.source_remove(this.#nextRefresh);
      this.#nextRefresh = undefined;
    }
  }

  #startNextMonitor() {
    // Calculates when the current next appointment is expired
    // and schedules a call to lookup the new next appointment, this takes into
    // consideration the "post hold" timing, so the next appointment stays next
    // after it has started.
    if (!this.enabled) return;

    this._clearNextRefresh();

    const now = new Date();
    const msec_until = this.msecUntilNext();

    if (isNaN(msec_until)) return;
    // Don't start a negative timer
    if (msec_until < 0) return;
    // Don't start a timer in more than a day, let the interval pick it up
    if (msec_until > DAY) return;

    console.log(
      `next refresh in ${msec_until / 1000 + this.postAppointmentHoldSec}s`,
    );
    const self = this;
    this.#nextRefresh = Utils.timeout(
      msec_until + this.postAppointmentHoldSec * 1000,
      function () {
        self._clearNextRefresh();
        self.getNext();
      },
    );
    return;
  }

  getAppointments() {
    return this.#appointments;
  }

  nextAppointmentSummary() {
    return this.#next.summary;
  }

  #formatCCDate(date) {
    // Helper for formatting a Date() to the input for calcurse
    const monthStr =
      date.getMonth() < 10
        ? `0${date.getMonth() + 1}`
        : `${date.getMonth() + 1}`;
    const dateStr =
      date.getDate() < 11 ? `0${date.getDate()}` : `${date.getDate()}`;
    return `${monthStr}/${dateStr}/${date.getFullYear()}`;
  }

  parseAppointments(query) {
    // Helper for looping over the calcurse query output
    // And parsing them into appointments, these are just objects with the summary
    // and start Date for each.
    if (query.length === 0) return [];

    return query
      .split("\n")
      .map(function (line) {
        if (!line.startsWith(PREFIX)) return undefined;

        const start = new Date(
          Number(line.split(" ", 1)[0].substr(PREFIX.length)) * 1000,
        );

        return {
          start: start,
          summary: line.substr(line.indexOf(" ") + 1),
        };
      })
      .filter(function (e) {
        return e !== undefined;
      });
  }

  #refreshAppointments() {
    // update the appointments list with all appointments
    // in calcurse for the current month
    if (!this.enabled) return;

    const today = new Date();
    // The start of the month is just the current month+year and a date of 1
    const start = this.#formatCCDate(
      new Date(today.getFullYear(), today.getMonth(), 1),
    );
    // The end is actually just going to be the first of the next month, which is:
    if (today.getMonth() === 11) {
      // Either the first month of the next year
      var end = this.#formatCCDate(new Date(today.getFullYear() + 1, 0, 1));
    } else {
      // Or the next month if it isn't the end of the year
      var end = this.#formatCCDate(
        new Date(today.getFullYear(), today.getMonth() + 1, 1),
      );
    }

    this.#appointments = this.parseAppointments(
      Utils.exec(
        "calcurse -Q --filter-type apt " +
          `--from ${start} --to ${end} ` +
          `--format-apt="${QUERY_FORMAT}"`,
      ),
    );
  }

  _updateNext(appointment) {
    // Helper to update and emit events when the next
    // appointment changes
    if (this.#next.start.valueOf() === appointment.start.valueOf()) return;

    this.#next.start = appointment.start;
    this.#next.summary = appointment.summary;
    console.log(
      `Next Appointment: ${this.#next.summary} @ ${this.#next.start}`,
    );
    this.emit("new-appointment", this.#next.start.valueOf());

    this.#startNextMonitor();
    const msec_until = this.msecUntilNext();
    this.#countdowns.forEach(function (cd) {
      cd.value = msec_until;
    });
  }

  getNext() {
    // lookup the next appointment on the calendar
    if (!this.enabled) return;

    const self = this;
    // For calcurse, we just look at the next 2 days for any appointments (including
    // recurring, I use recurring appointments for daily reminders).  Then remove
    // any appointments that already have happened.  Emitting state changes as
    // needed
    Utils.execAsync(
      `calcurse -Q --filter-type cal --day 2 --format-apt="${QUERY_FORMAT}" --format-recur-apt="${QUERY_FORMAT}"`,
    )
      .then(function (query) {
        const now = new Date();
        // Parse the appointments from the query, getting the first one that hasn't
        // happened
        const appointment = self.parseAppointments(query).find(function (appt) {
          return (
            appt.start.valueOf() + self.postAppointmentHoldSec * 1000 >
            now.valueOf()
          );
        });
        // If there is one, trigger the update/emitting
        if (appointment) return self._updateNext(appointment);
        // Otherwise emit stuff with the default values
        return self._updateNext({
          start: new Date(MAX_DATE_VAL),
          summary: "Nothing",
        });
      })
      .catch(function (err) {
        console.log(`Err: ${err}`);
      });
  }

  refresh(_) {
    if (!this.enabled) return;
    this.#refreshAppointments();
    this.getNext();
  }
}

// the singleton instance
const service = new CalcurseService();

export default service;
