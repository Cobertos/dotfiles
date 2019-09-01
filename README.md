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
 * 

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

## Future Support
* WSL Install/Enable
* Voicemeeter Banana
* Setup correct file associations (for .xml, .html, etc...)

## Tools that just need installation
* Ino Reader (part of Chrome extensions
* Unity-Hub (broken on Chocolatey)
* Paint.NET and Spotify are installed through Windows App Store (wanted to try that out)
* Blender is installed separately (managing multiple Blender versions)
* `pyenv` for managing multiple versions of Python
