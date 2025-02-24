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
    results = []
    for hook in after_hooks:
        if dry_run:
            print(f"Would Run: {hook.__name__}")
            continue
        # We want to eat any failures up front so one broken after hook doesn't
        # skip all the others, then re-raise a failure
        try:
            hook()
        except BaseException as e:
            print(f"Hook {hook.__name__} failed: {e}")
            results.append(e)

    if len(results):
        # Only raising the first, but would be nice to raise all of them?
        raise results[0]
