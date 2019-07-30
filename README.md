# Dot Files

A collection of configs and dot files for programs I use on Windows.

* **Public** - Private keys and licenses are separate (for now...)
* **Automatic** - `python setup.py` sets up everything. `--verify-only` will verify an install without performing any operation
* **Console** - Only console dev related configs live in here (everything else in Dropbox for now...)
* **Portable** - Use different configs ending in `##XXX` suffix with `--environment=XXX` flag
* **Linking** - Symlinks over copying

**Requires Python 3.6+ (interpolated literals and other fun things)**

## Installation

* `python setup.py`
 * `--verify-only` - Lets you know the state of all the links, path operations, etc without doing anything
 * `--environment=XXX` - Uses files ending in `##XXX` if they exist instead

## Currently supports

* [Git for Windows](https://git-scm.com/download/win)
* [Sublime Text](https://www.sublimetext.com/3)
* [ConEmu](https://conemu.github.io/en/Downloads.html)
* WSL

* Paint.NET
* Blender

## Tools that just need installation
(maybe move to Chocolatey?)
(TODO: Move to chocolatey when packages.config export is a thing, otherwise it's kind of useless for my workflow)
* 7zip
* Dropbox
* Lastpass
* Chrome
* Firefox
* Discord
* Standard Notes
* Git for Windows
* VLC Media Player
* Ino Reader
* FooBar 3000
* OpenHardwareMonitor
* OBS
* Unity
* ShareX

## To Add

* Python 3 (and associated linters)
* NodeJS (and associated linters) (probably better to install nvm)
* Paint.NET
* Any other useful programs or scripts