from shutil import which

if which("streamlink"):
    c.aliases["stream"] = "spawn streamlink {url}"

if which("wezterm"):
    c.editor.command = [
        "wezterm", "start", "vim -f {file} -c normal {line}G{column0}"
    ]
elif which("alacritty"):
    c.editor.command = [
        "alacritty", "--command", "vim -f {file} -c normal {line}G{column0}"
    ]

if which("xdg-open"):
    c.aliases["xopen"] = "spawn xdg-open {url}"
