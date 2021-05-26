# jdost's configs

This is my dotfiles repo along with setup handling scripting.  The main
purpose is to allow defining various assets required for setting up
different "things", meaning config files, packages, symlinks, wrapper
scripts, system settings, etc.

## Usage

The `setup` script will invoke the setup logic for any input modules.  If
no module is input it will run `systems.<HOSTNAME>` if it exists (or error
out).

## Configuration definitions

All of the folders are meant to be python modules and the setup
declaration lives in the `__init__.py` file in each folder.  These then
utilize more functional definitions under the `cfgtools` folder which is
where the actual handling for the declarations lives.  The definitions are
mostly just package definitions (with specific handlers for various
variants for each distro) and files.

### Packages

For packages, there are a growing list of types:
- `arch.Pacman` - Normal Arch Linux based packages
- `arch.AUR` - User respository definitions for arch, these use the `aur`
  wrapper for building the packages via docker
- `python.VirtualEnv` - Python package installation within a user local
  virtualenv
- `ubuntu.Apt` - Normal Ubuntu provided packages

Most of the underlying logic for these handle determining if anything
declared is uninstalled and attempting to install them.  These are meant
to be no-ops if previously run and to try and determine any delta between
their expected state, but are probably missing bits.

### Files

For files, all are based on `File` which handles creating a symlink from
a local file definition to a destination if it doesn't exist and
associated logic on whether the destination exists but is pointing
somewhere else.

There are then a variety of helpers for different types/patterns like
user binaries (`~/.local/bin/`), user environment extensions
(`~/.local/environment`), xinitrc extensions
(`~/.config/xorg/xinitrc.d/`), etc.  Extending/adding new ones is
pretty easy and all ends up leveraging the base generic definition.

### Misc

There are then a variety of smaller helpers and hooks.  There are the
`@before` and `@after` decorators that can declare hooks to run things
before or after the bulk of actions (file and package operations).  Then
there are a number of smaller helper functions that these hooks can use,
like enabling/disable user systemd units, changing the user's default
shell, adding the user to a group, etc.

## Profiles

The rest of the folders beyond `cfgtools` are module declarations except
for `systems` which are instead full of collections for different systems.
These just import all the default modules for each system and any
additional file overrides (which are often added as support for
various modules).  Each folder is mapped to the hostname of the system
and is the default target of the `setup` helper.
