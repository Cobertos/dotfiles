# Dot Files

A collection of configs and dot files for programs I use on Windows.

* **Public** - Private keys and licenses are separate (for now...)
* **Automatic** - `python setup.py` sets up everything. `--verify-only` will verify an install without performing any operation
* **Console** - Only console dev related configs live in here (everything else in Dropbox for now...)
* **Portable** - Use different configs ending in `##XXX` suffix with `--environment=XXX` flag
* **Linking** - Symlinks over copying

## Installation
* [Install chocolatey](https://chocolatey.org/docs/installation)
 * I would like to automate this but there's a lot of overhead with Python)
* `choco install ./packages.config`
* Install Python 3.6+ (requires at least 3.6 because of interpolated literals, f"")
* `python setup.py`
 * `--verify-only` - Lets you know the state of all the links, path operations, etc without doing anything
 * `--environment=XXX` - Uses files ending in `##XXX` if they exist instead

## Supports
* Everything in `packages.config` (run `scripts/chocoConfig.py` to regenerate!)
 * Git for Windows configurations
 * Sublime Text 3 configurations
  * You need to manually setup license for it and SFTP though!
 * BashRC
 * ConEmu configurations
 * Paint.NET configurations

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
* Uninstall unwanted default apps
* Connect phone to My Phone
* Login to other Microsoft related products
* Setup TabNine (TabNine::Config then paste key for TabNine Local)
* Install eslint_d and other things for Sublime packages
* Install office
* Set surface pen pressure to like 8-9?
* Install Unity-Hub (broken on Chocolatey)
* Install Windows App Store apps (including Paint.NET and Spotify)
* Ino Reader (part of Chrome extensions)
* Blender is installed separately (managing multiple Blender versions)
* `pyenv` for managing multiple versions of Python
* Remove Python execution aliases
 * https://superuser.com/questions/1437590/typing-python-on-windows-10-version-1903-command-prompt-opens-microsoft-stor

## Future Support
* WSL Install/Enable
* Voicemeeter Banana
* Setup correct file associations (for .xml, .html, etc...)
* Global packages for node.js and python
* Choco git installation requires custom flags (which I didn't notate...)
* VLC Plugins
* Audacity and configurations
* Verify and install npm packages globally
 * `@vue/cli`
 * `eslint_d`
 * `serverless`
 * `lessmd`
 * Windows build tools?
* Verify and install pip packages
 * `yamllint`
 