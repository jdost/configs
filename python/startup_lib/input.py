import enum
import readline
import rlcompleter
import sys

_CSI = "\033["


class COLORS(str, enum.Enum):
    BLACK = f"{_CSI}30m"
    RED = f"{_CSI}31m"
    GREEN = f"{_CSI}32m"
    YELLOW = f"{_CSI}33m"
    BLUE = f"{_CSI}34m"
    MAGENTA = f"{_CSI}35m"
    CYAN = f"{_CSI}36m"
    WHITE = f"{_CSI}37m"
    RESET = f"{_CSI}39m"


class IndentableCompleter(rlcompleter.Completer):
    INDENT = " " * 4
    def complete(self, text: str, state: int) -> str:
        return [self.INDENT, None][state] if text == '' or text.isspace() else \
            super().complete(text, state)


class ColoredPS:
    C_SEQ = [COLORS.RED, COLORS.GREEN, COLORS.YELLOW, COLORS.BLUE, COLORS.MAGENTA,
             COLORS.CYAN, COLORS.WHITE]

    def __init__(self, seq: str):
        self.seq = seq
        self.count = 0

    def __str__(self) -> str:
        fg = self.C_SEQ[self.count % len(self.C_SEQ)]
        self.count += 1
        return f"{fg}{self.seq}{COLORS.RESET} "


def setup_tabcomplete() -> None:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(IndentableCompleter().complete)

    sys.ps1 = ColoredPS(">>>")
    sys.ps2 = ColoredPS("...")
