from shutil import which

if which("streamlink"):
    c.aliases["stream"] = "spawn streamlink {url}"

if which("alacritty"):
    c.editor.command = [
        "alacritty", "--command", "vim -f {file} -c normal {line}G{column0}"
    ]
