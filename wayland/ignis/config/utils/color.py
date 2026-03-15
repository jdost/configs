class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: float = 1.0) -> None:
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def as_rgb(self) -> str:
        return f"rgb({self.red}, {self.green}, {self.blue})"

    def as_rgba(self) -> str:
        return f"rgb({self.red}, {self.green}, {self.blue}, {self.alpha})"

    def with_alpha(self, alpha) -> "Color":
        return Color(self.red, self.green, self.blue, alpha)


YELLOW = Color(255, 255, 0)
ORANGE = Color(255, 153, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
CYAN = Color(85, 170, 255)
WHITE = Color(255, 255, 255)
GREY = Color(100, 100, 100)
