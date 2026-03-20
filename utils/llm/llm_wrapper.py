#!/usr/bin/env python3
"""
Convenience wrapper for the `llm` CLI tool.

The main purpose of this is to make the `--conversation-id` system sensible by
taking a variant argument set of `--chat` to alias converations to memorable
names.  This just attempts to store the alias to real ID lookup when new or
will translate the arguments to the accepted format.

Works by manipulating the python path.
"""

import sys
from pathlib import Path

# Extract the MAJOR.MINOR python version to interpolate into the path
python_version = f"python{sys.version.split(' ')[0].rsplit('.', 1)[0]}"
# Make path high precedence, as it will clash with this configs repo
sys.path.insert(0, str(Path.home() / f".local/llm/lib/{python_version}/site-packages"))


import json

from llm.cli import cli

CHAT_LOOKUP_FILE = Path.home() / ".config/io.datasette.llm/lookup_helper.json"


def get_chat_aliases() -> dict[str, str]:
    if not CHAT_LOOKUP_FILE.exists():
        return {}

    return json.loads(CHAT_LOOKUP_FILE.read_text())


def store_chat_alias(chat_id: str, alias: str) -> None:
    chats = get_chat_aliases()
    chats[alias] = chat_id
    CHAT_LOOKUP_FILE.write_text(json.dumps(chats))


def chat_ids() -> set[str]:
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(cli, ["logs", "list", "--json"])

    return [c["id"] for c in json.loads(result.output)]


if __name__ == "__main__":
    args = sys.argv[1:]
    new_chat_alias = None

    for i, arg in enumerate(args):
        if arg == "--chat":
            chat_alias = args[i + 1]
            alias_lookups = get_chat_aliases()
            if chat_alias not in alias_lookups:
                print(
                    f"No id found for {chat_alias}, will store new conversation for it..."
                )
                new_chat_alias = chat_alias
                args = [*args[:i], *args[i + 2 :]]
            else:
                args = [*args[:i], "--conversation", *args[i + 2 :]]
            break

    before_chat_ids = set()
    if new_chat_alias:
        before_chat_ids = {*chat_ids()}

    try:
        cli(args)
    finally:
        if new_chat_alias:
            new_chat_ids = {*chat_ids()} - before_chat_ids
            if not new_chat_ids:
                print(f"Nothing started to aliase to {chat_alias}...")
            else:
                store_chat_alias(list(new_chat_ids)[0], chat_alias)
                print(
                    f"Storing {list(new_chat_ids)[0]} under the alias {chat_alias}..."
                )
