from typing import Callable, List

before_hooks: List[Callable[[], None]] = []
after_hooks: List[Callable[[], None]] = []


def before(func: Callable[[], None]) -> Callable[[], None]:
    if func not in before_hooks:
        before_hooks.append(func)

    return func


def after(func: Callable[[], None]) -> Callable[[], None]:
    if func not in after_hooks:
        after_hooks.append(func)

    return func


def run_before(dry_run: bool = False) -> None:
    for hook in before_hooks:
        if dry_run:
            print(f"Would Run: {hook.__name__}")
        else:
            hook()


def run_after(dry_run: bool = False) -> None:
    for hook in after_hooks:
        if dry_run:
            print(f"Would Run: {hook.__name__}")
        else:
            hook()
