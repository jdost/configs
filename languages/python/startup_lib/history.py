import atexit
import os
import readline

from pathlib import Path


def get_histfile() -> Path:
    if "PYTHONHISTFILE" in os.environ:
        return Path(os.environ["PYTHONHISTFILE"])
    if "XDG_DATA_HOME" in os.environ:
        return Path(os.environment["XDG_DATA_HOME"]) / "python_history"

    return Path.home() / ".local/share/python_history"


def save_history(start_index: int, length: int, histfile: Path) -> None:
    end_index = readline.get_current_history_length()
    readline.set_history_length(length)
    readline.append_history_file(end_index - start_index, histfile)


def setup_histfile(history_length: int = 1000) -> None:
    histfile = get_histfile()

    try:
        readline.read_history_file(histfile)
        start_index = readline.get_current_history_length()
    except FileNotFoundError:
        open(histfile, "wb").close()
        start_index = 0

    atexit.register(save_history, start_index, history_length, histfile)
