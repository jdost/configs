from typing import Callable, Iterable

from ignis import widgets
from ignis.gobject import IgnisGObject, IgnisSignal
from ignis.utils import Timeout

from utils.transitions import Transition, enabled

SINGLE_CHILD_WIDGETS = {widgets.Button, widgets.Overlay}


def isiterable(var: object) -> bool:
    return isinstance(var, Iterable) and hasattr(var, "__len__")


def binding(hook: str) -> Callable[[Callable], Callable]:
    def register[T](method: T) -> T:
        setattr(method, "binding", hook)
        return method

    return register


class BaseWidget(IgnisGObject):
    name: str = "unnamed"

    base: type[widgets.Widget]
    # List of class properties that get passed to the widget constructor
    __build_props__: set[str] = {
        "css_classes",
        "spacing",
        "valign",
        "halign",
        "hexpand",
        "vexpand",
        "tooltip_text",
        "sensitive",
        "visible",
        "width_request",
        "height_request",
        "style",
        "cursor",
    }
    # This maps object methods to action callbacks
    __action_bindings__: set[str] = {
        "setup",
        "on_click",
        "on_right_click",
    }
    on_show: Transition | None = None
    on_hide: Transition | None = None
    widget: None | widgets.Widget
    revealers: list[widgets.Revealer | None]

    def __init__(self, *args, **kwargs):
        self.widget = None
        self.revealers = [None, None]
        super().__init__(*args, **kwargs)

    @IgnisSignal
    def destroyed(self) -> None:
        pass

    def unparent(self) -> None:
        for tgt in [self.widget, *self.revealers]:
            if not tgt:
                continue
            tgt.unparent()

    def destroy(self) -> None:
        def cleanup():
            for tgt in [self.widget, *self.revealers]:
                if not tgt:
                    continue
                tgt.unrealize()

            if hasattr(self, "on_destroy"):
                self.on_destroy()

            # Clear the refs after calling the on_destroy hook in case other
            # cleanup is necessary (like unparenting)
            self.widget = None
            self.revealers = [None, None]
            self.emit("destroyed")

        if enabled and self.on_hide:
            if self.revealers[1]:
                self.revealers[1].reveal_child = False
            Timeout(ms=self.on_hide.duration, target=cleanup)
            return

        cleanup()

    def render(self, *args, **kwargs: object) -> widgets.Widget:
        if not hasattr(self, "base"):
            raise ValueError("Need to declare a widget type.")

        for prop in self.__build_props__:
            if hasattr(self, prop):
                kwargs[prop] = getattr(self, prop)

        for binding in self.__action_bindings__:
            if hasattr(self, binding) and callable(getattr(self, binding)):
                action = getattr(self, binding)
                kwargs[
                    getattr(action, "binding")
                    if hasattr(action, "binding")
                    else binding
                ] = action

        is_single_child = self.base in SINGLE_CHILD_WIDGETS

        if hasattr(self, "child"):
            if isiterable(self.child) and is_single_child:
                raise ValueError("Cannot have multiple children")
            elif isiterable(self.child):
                kwargs["child"] = [c.render() for c in self.child]
            elif is_single_child:
                kwargs["child"] = self.child.render()
            else:
                kwargs["child"] = [self.child.render()]
        elif hasattr(self, "children"):
            if is_single_child:
                raise ValueError("Cannot have multiple children")
            kwargs["child"] = [c.render() for c in self.children]
        elif hasattr(self, "render_children") and callable(self.render_children):
            if is_single_child:
                raise ValueError("Cannot have multiple children")
            kwargs["child"] = self.render_children()
        elif hasattr(self, "render_child") and callable(self.render_child):
            child = self.render_child()
            if is_single_child and isiterable(child):
                raise ValueError("Cannot have multiple children")
            elif is_single_child:
                kwargs["child"] = child
            else:
                kwargs["child"] = child if isiterable(child) else [child]

        self.widget = self.base(*args, **kwargs)
        target = self.widget
        self.revealers = [None, None]

        if self.on_show:
            self.revealers[0] = widgets.Revealer(
                child=target,
                transition_type=self.on_show.animation,
                transition_duration=self.on_show.duration,
                reveal_child=not enabled,
            )

            def reveal() -> None:
                if self.revealers[0]:
                    self.revealers[0].reveal_child = True

            target = self.revealers[0]
            Timeout(ms=50, target=reveal)
        if self.on_hide:
            self.revealers[1] = widgets.Revealer(
                child=target,
                transition_type=self.on_hide.animation,
                transition_duration=self.on_hide.duration,
                reveal_child=True,
            )
            target = self.revealers[1]

        return target
