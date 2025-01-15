import { Color } from "./color.js";
const DOTS = [..."⡀⠄⠂⠁"];

export const LevelDots = function (audio_device) {
  return Widget.Box({
    class_name: "leveldot-container",
    children: [
      Widget.Overlay({
        class_name: "leveldot",
        child: Widget.Label(DOTS[0]),
        attribute: audio_device,
        overlays: DOTS.map(Widget.Label),
      }).hook(audio_device, function (self) {
        if (audio_device.stream === null) return;

        self.tooltip_text = audio_device.stream.is_muted
          ? "Volume: Muted"
          : `Volume: ${Math.ceil(audio_device.volume * 100)}%`;

        const volume = audio_device.stream.is_muted ? 0.0 : audio_device.volume;
        for (var i = 1; i <= self.overlays.length; i++) {
          const index = i - 1;
          if (i > Math.ceil(volume * 4)) {
            self.overlays[index].css = "opacity: 0;";
            continue;
          }
          if (i === Math.ceil(volume * 4)) {
            const calcOpac = (volume * 4) % 1;
            self.overlays[index].css =
              `opacity: ${calcOpac == 0 ? 1 : calcOpac};`;
          } else {
            self.overlays[index].css = "opacity: 1.0;";
          }
        }
      }),
    ],
  });
};

const GRADIENT = [Color(0, 204, 0), Color(255, 255, 0), Color(255, 0, 0)];

export const calcGradientColor = function (gradient, value) {
  if (value > 1.1) {
    console.log(
      "ERROR: calcGradientColor only takes floating point between 0.0 and 1.0",
    );
    return;
  }
  const gradientLevel = value * (gradient.length - 1);
  if (gradientLevel / 1 === 0) {
    return gradient[gradientLevel].as_rgb();
  }

  const low = gradient[Math.floor(gradientLevel)] || gradient[0];
  const high =
    gradient[Math.ceil(gradientLevel)] || gradient[gradient.length - 1];
  return Color(
    Math.round(low.red + (high.red - low.red) * (gradientLevel % 1)),
    Math.round(low.green + (high.green - low.green) * (gradientLevel % 1)),
    Math.round(low.blue + (high.blue - low.blue) * (gradientLevel % 1)),
  ).as_rgb();
};

export const GradientIcon = function (label, name, levelBinding) {
  return Widget.Label({
    class_name: name,
    label: label,
    tooltip_text: levelBinding.as(function (level) {
      return `${name}: ${level.toFixed(2)}%`;
    }),
    css: levelBinding.as(function (level) {
      if (level === NaN) {
        return;
      }

      return `color: ${calcGradientColor(GRADIENT, level / 100)};`;
    }),
  });
};
