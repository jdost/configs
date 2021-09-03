#!/usr/bin/env python3

import os
import re
import sys

from pathlib import Path
from shutil import which

browsers = [
    "qutebrowser",
    "firefox",
    "chromium",
]
target_browser = ""
url = sys.argv[1]

XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
for browser_config in (XDG_CONFIG_HOME / "web-xdg-open").iterdir():
    values = browser_config.read_text().split("\n")
    name = values[0]
    if not which(name):
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

if target_browser and not which(target_browser):
    target_browser = ""

if not target_browser:
    for browser in browsers:
        if which(browser):
            target_browser = browser
            break

if not target_browser:
    sys.exit("No browser installed from expected list.")

args = [url]
print(repr([which(target_browser), *args]))
os.execl(which(target_browser), target_browser, *args)
