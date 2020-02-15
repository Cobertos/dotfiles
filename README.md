# Dot Files

A collection of configs and dot files for programs I use on Windows.

* **Public** - Private keys and licenses are separate (for now...)
* **Automatic** - `python setup.py` sets up everything. `--verify-only` will verify an install without performing any operation and is eventually meant to be used every time I boot my machine or something...
* **Console** - Only console dev related configs live in here (everything else in Dropbox for now...)
* **Portable** - Use different configs ending in `##XXX` suffix with `--environment=XXX` flag
* **Linking** - Symlinks over copying

## Installation
* [Install chocolatey](https://chocolatey.org/docs/installation)
 * I would like to automate this but there's a lot of overhead with Python)
* `choco install ./packages.config`
* Install `pyenv` by downloading and extracting at the correct location and setting up variables
* Install Python 3.6+ (requires at least 3.6 because of interpolated literals, f"")
* Install Dropbox (fails if not installed, TODO) and make sure nvm is using a version of npm (fails if not installed, TODO)
* Make a .bashrc if not exists (fails currently, TODO)
* `python bootstrap/cli.py` (There's a `--help` now)
 * Make sure to use the right `--environment=XXX`!

## Supports
* Look at `packages.config`, `bootstrap/cli.py`, and `cobertos.bashrc` for what's supported

## You need to manually
* Install Chrome
 * Login to Chrome
 * Login to Lastpass
 * Login to InoReader
* Windows settings
 * Turn off sticky keys and other accessibility
 * Turn off mouse precision
 * Setup custom theme including wallpapers, lockscreen, sounds
 * Turn off device rotation
 * Enable file extensions and hidden files in Explorer
* Dropbox selective sync large folders
* Spotify download playlists
* Install package control in Sublime to get it to recognize packages
* Setup license for Sublime and FTP
* Uninstall unwanted default apps
* Connect phone to My Phone
* Login to other Microsoft related products
* Setup TabNine (TabNine::Config then paste key for TabNine Local)
* Install office
* Set surface pen pressure to like 8-9?
* Install Unity-Hub (broken on Chocolatey)
* Install Windows App Store apps (including Paint.NET and Spotify)
* Blender is installed separately (managing multiple Blender versions)
* Remove Python execution aliases
 * https://superuser.com/questions/1437590/typing-python-on-windows-10-version-1903-command-prompt-opens-microsoft-stor
* Configure explorer preferences (hidden files and exteions)
* Configure taskbar preferences (non grouping etc)
* Turn off Windows sounds (the default sounds)
* Communication 80% decrease turn off 
* Remove certain pins from the taskbar
* Make backspace faster/proper speed
* Setup conemu here manually

## Future Support
* WSL Install/Enable
* Voicemeeter Banana
* Setup correct file associations (for .xml, .html, etc...)
* Choco git installation requires custom flags (which I didn't notate...)
* VLC Plugins
* Audacity and configurations
* A separate packages.config for different workflows
* Add symbolic links to Dropbox bin/ folder (requires a Symlink to the Dropbox folder)
 * Move the ones that support it form the tools folder into Chocolatey
* ShareX config
* Installing chocolatey packages
* Make sure that Chrome syncs settings for refined GitHub (looks like it worked)
* Rust

## TODO
* Delete a bunch of cruft in the users folder for explorer
* Find a better explorer (I heard there was a nice one)
* Change windows bootup art and other shit like my phone
* Add a console startup message owo
* TODO: Computer name
* Add z's config (but somehow without leaking all the path names, or don't...)

* Yamllint isnt installed but it says it is