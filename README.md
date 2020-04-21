# Dot Files

A collection of configs and dot files for programs I use on Windows and Linux.

* **Public** - Private keys and licenses are separate (for now...)
* **Automatic** - `python setup.py` sets up everything. `--verify-only` will verify an install without performing any operation and is eventually meant to be used every time I boot my machine or something...
* **Console** - Only console dev related configs live in here (everything else in Dropbox for now...)
* **Portable** - Use different configs ending in `##XXX` suffix with `--environment=XXX` flag
* **Linking** - Symlinks over copying

## Installation
* Linux
```bash
sudo apt install git ansible
git clone https://github.com/davestephens/ansible-playbook-ubuntu-dev-desktop.git && cd ansible-playbook-ubuntu-dev-desktop
ansible-galaxy install -r requirements.yml
ansible-playbook desktop.yml
```
* Windows
* Install Ansible in WSL
* Do https://stackoverflow.com/questions/58345011/setup-windows-10-workstation-using-ansible-installed-on-wsl
* Follow the above linux inatructions

## Installation Old
* Install `pyenv` by downloading and extracting at the correct location and setting up variables
* Install Python 3.6+ (requires at least 3.6 because of interpolated literals, f"")
* Install Dropbox (fails if not installed, TODO) and make sure nvm is using a version of npm (fails if not installed, TODO)
* Make a .bashrc if not exists (fails currently, TODO)
* `python bootstrap/cli.py` (There's a `--help` now)
 * Make sure to use the right `--environment=XXX`!

## You need to manually
* Install office (TODO: https://chocolatey.org/packages/office-tool#files)
* Login to Chrome, Lastpass, InoReader, Dropbox, Microsoft related products (office)
* Windows settings
 * Turn off device rotation
 * Lockscreen picture
 * Uninstall unwanted default apps
 * Connect phone to My Phone
 * Set surface pen pressure to like 8-9?
 * Configure taskbar preferences (non grouping etc)
 * Remove certain pins from the taskbar
 * Make backspace faster/proper speed
 * Remove OneDrive
 * Rename computer
 * Install Windows App Store apps (including Paint.NET and Spotify)
 * Remove Python execution aliases (no way to do it from cmd found yet)
  * https://superuser.com/questions/1437590/typing-python-on-windows-10-version-1903-command-prompt-opens-microsoft-stor
* Dropbox
 * Turn off dropbox notifications (so certain files dont unexpectedly popup...)
 * Selectively sync proper folders
 * TODO: Switch to Seafile to use an ignore file
* Spotify
 * Download playlists
* Sublime
 * Install package control to recognize symlinked packages
 * Install license and license for FTP
 * Setup TabNine (TabNine::Config then paste key for TabNine Local)
* Install Unity-Hub (broken on Chocolatey)
* Blender is installed separately (managing multiple Blender versions)
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
* Make sure that Chrome syncs settings for refined GitHub (looks like it worked)
* Rust

## TODO
* Hide excess folders I don't use anymore like 3D Objects, etc... (they're all in dropbox now)
* Add z's config (but somehow without leaking all the path names, or don't...)