from dataclasses import dataclass

enabled = True


@dataclass
class Transition:
    animation: str
    duration: int

    def __init__(self, duration: int) -> None:
        self.duration = duration


class CrossFade(Transition):
    animation = "crossfade"


class SlideRight(Transition):
    animation = "slide_right"


class SlideLeft(Transition):
    animation = "slide_left"


class SlideUp(Transition):
    animation = "slide_up"


class SlideDown(Transition):
    animation = "slide_down"


class SwingRight(Transition):
    animation = "swing_right"


class SwingLeft(Transition):
    animation = "swing_left"


class SwingUp(Transition):
    animation = "swing_up"


class SwingDown(Transition):
    animation = "swing_down"
