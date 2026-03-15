from typing import Callable, Iterable

from ignis import widgets

SINGLE_CHILD_WIDGETS = {widgets.Button, widgets.Overlay}


def isiterable(var: object) -> bool:
    return isinstance(var, Iterable) and hasattr(var, "__len__")


def binding(hook: str) -> Callable[[Callable], Callable]:
    def register[T](method: T) -> T:
        setattr(method, "binding", hook)
        return method

    return register


class BaseWidget:
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
        return self.widget
