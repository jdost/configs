import { add_right } from "../widgets/bar.js";

const time = Variable("", {
  poll: [1000, 'date "+%H:%M:%S"'],
});
const date = Variable("", {
  poll: [60 * 1000, 'date "+%A, %x"'],
});

add_right(
  Widget.Label({
    class_name: "clock",
    label: time.bind(),
    tooltip_text: date.bind(),
  }),
  false,
);
