# Let's inject our collection of helpers into the import path
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

# history file
from startup_lib import history

HISTORY_LENGTH = 5000
history.setup_histfile(HISTORY_LENGTH)

# input configuration
from startup_lib import input as input_lib

input_lib.setup_tabcomplete()

# cleanup
del sys, Path, history, HISTORY_LENGTH, input_lib
