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
        return f"{fg.value}{self.seq}{COLORS.RESET.value} "


def setup_tabcomplete() -> None:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(IndentableCompleter().complete)

    sys.ps1 = ColoredPS(">>>")
    sys.ps2 = ColoredPS("...")


def autoindent() -> None:
    """Auto-indent upon typing a new line according to the contents of the
    previous line.  This function will be used as Readline's
    pre-input-hook.

    """
    hist_len = readline.get_current_history_length()
    last_input = readline.get_history_item(hist_len)
    try:
        last_indent_index = last_input.rindex("    ")
    except Exception:
        last_indent = 0
    else:
        last_indent = int(last_indent_index / 4) + 1

    if len(last_input.strip()) > 1:
        if last_input.count("(") > last_input.count(")"):
            indent = ''.join(["    " for n in range(last_indent + 2)])
        elif last_input.count(")") > last_input.count("("):
            indent = ''.join(["    " for n in range(last_indent - 1)])
        elif last_input.count("[") > last_input.count("]"):
            indent = ''.join(["    " for n in range(last_indent + 2)])
        elif last_input.count("]") > last_input.count("["):
            indent = ''.join(["    " for n in range(last_indent - 1)])
        elif last_input.count("{") > last_input.count("}"):
            indent = ''.join(["    " for n in range(last_indent + 2)])
        elif last_input.count("}") > last_input.count("{"):
            indent = ''.join(["    " for n in range(last_indent - 1)])
        elif last_input[-1] == ":":
            indent = ''.join(["    " for n in range(last_indent + 1)])
        else:
            indent = ''.join(["    " for n in range(last_indent)])
    readline.insert_text(indent)


def setup_autoindent() -> None:
    readline.set_pre_input_hook(autoindent)
