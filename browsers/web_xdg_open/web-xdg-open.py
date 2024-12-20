#!/usr/bin/env python3

import os
import re
import shlex
import sys
from pathlib import Path
from shutil import which
from typing import Sequence, Union

browsers = [
    "qutebrowser",
    "firefox",
    "chromium",
]
target_browser: Sequence[Union[str, Path]] = []
XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
default_browser = (XDG_CONFIG_HOME / "web-xdg-open/default").resolve()
lookup = False

for arg in sys.argv:
    if arg == "--lookup":
        lookup = True
    else:
        url = arg

for browser_config in (XDG_CONFIG_HOME / "web-xdg-open").iterdir():
    if browser_config.name == "default":
        continue

    values = browser_config.read_text().split("\n")
    name = shlex.split(values[0])
    if not which(name[0]):
        continue

    for url_test in values[1:]:
        if not url_test:
            continue
        if url_test.startswith("re:"):
            if re.match(url_test[3:], url):
                target_browser = name
                break
        else:
            if re.search(url_test, url):
                target_browser = name
                break

    if target_browser:
        break

if target_browser and not which(target_browser[0]):
    target_browser = []

if not target_browser:
    if default_browser.exists():
        target_browser = [default_browser]
    else:
        for browser in browsers:
            if which(browser):
                target_browser = [which(browser)]
                break

if len(target_browser) == 0:
    sys.exit("No browser installed from expected list.")

if len(target_browser) > 1:
    args = [*target_browser[1:], url]
else:
    args = [url]

if isinstance(target_browser[0], str):
    target_browser_path = Path(which(target_browser[0]))
else:
    target_browser_path = target_browser[0]

assert target_browser_path is not None

if lookup:
    print(" ".join([str(target_browser[0]), *args]))
else:
    os.execl(target_browser_path, target_browser[0], *args)
