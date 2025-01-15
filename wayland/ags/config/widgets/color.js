/**
 * Color is a helper type for color manipulation a logic.  Wraps the `rgba` with
 * appropriate types and provides various output helpers for both string output and
 * extra manipulation.
 **/
export function Color(r, g, b, a) {
  const red = r === undefined ? 255 : r;
  const green = g === undefined ? 255 : g;
  const blue = b === undefined ? 255 : b;
  const alpha = a === undefined ? 1.0 : a;

  // toString methods
  const as_rgba = function as_rgba() {
    return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
  };
  const as_rgb = function as_rgb() {
    return `rgb(${red}, ${green}, ${blue})`;
  };
  // Helper for generating a variant of the color with an alpha override
  const with_alpha = function with_alpha(a) {
    return Color(red, green, blue, a);
  };

  return {
    red: red,
    green: green,
    blue: blue,
    as_rgba: as_rgba,
    as_rgb: as_rgb,
    with_alpha: with_alpha,
    toString: as_rgba,
  };
}

// Export sane defaults for various colors
export const YELLOW = Color(255, 255, 0);
export const ORANGE = Color(255, 153, 0);
export const RED = Color(255, 0, 0);
export const CYAN = Color(85, 170, 255);
export const WHITE = Color(255, 255, 255);

export default Color = Color;
