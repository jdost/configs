import builtins
import sys
from pprint import pprint
from typing import Any


def setup_pprint() -> None:
    def displayhook(v: Any, show=pprint, bltin=builtins) -> None:
        if v is None:
            return
        bltin._ = v
        show(v)

    sys.displayhook = displayhook
