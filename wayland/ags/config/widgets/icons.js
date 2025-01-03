const DOTS = [..."⡀⠄⠂⠁"];

export const LevelDots = function (audio_device) {
  return Widget.Overlay({
    class_name: "leveldot",
    child: Widget.Label({ label: DOTS[0] }),
    overlays: DOTS.map(function (c) {
      return Widget.Label({ label: c });
    }),
    setup: function (self) {
      self.hook(audio_device, function () {
        if (audio_device.stream === null) return;

        if (audio_device.stream.is_muted) self.tooltip_text = "Volume: Muted";
        else
          self.tooltip_text = `Volume: ${Math.ceil(audio_device.volume * 100)}%`;
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
      });
    },
  });
};

const GRADIENT = [
  [0, 204, 0],
  [255, 255, 0],
  [255, 0, 0],
];

function toColor([r, g, b]) {
  return `rgb(${r}, ${g}, ${b})`;
}

export const calcGradientColor = function (gradient, value) {
  if (value > 1.1) {
    console.log(
      "ERROR: calcGradientColor only takes floating point between 0.0 and 1.0",
    );
    return;
  }
  const gradientLevel = value * (gradient.length - 1);
  if (gradientLevel / 1 === 0) {
    return toColor(gradient[gradientLevel]);
  }

  const low = gradient[Math.floor(gradientLevel)] || gradient[0];
  const high =
    gradient[Math.ceil(gradientLevel)] || gradient[gradient.length - 1];
  var color = [
    Math.round(low[0] + (high[0] - low[0]) * (gradientLevel % 1)),
    Math.round(low[1] + (high[1] - low[1]) * (gradientLevel % 1)),
    Math.round(low[2] + (high[2] - low[2]) * (gradientLevel % 1)),
  ];

  return toColor(color);
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
