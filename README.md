# Dot Files

A collection of configs and dot files for programs I use on Windows and Linux.

* **Public** - Private keys and licenses are separate (for now...)
* **Automatic** - `ansible-playbook ansible-main.yml` sets up everything. `--check` will verify an install without performing any operation and is eventually meant to be used every time I boot my machine or something...
* **Console** - Only console dev related configs live in here (everything else in Dropbox for now...)
* **Portable** - Use different configs ending in `##XXX` suffix with `-e dotfiles_env=XXX` flag
* **Cross Platform** - Work on Windows _and_ Linux
* **Linking** - Symlinks over copying

## Installation
* Linux
```bash
sudo apt install git ansible
git clone https://github.com/Cobertos/dotfiles.git && cd dotfiles
ansible-playbook ansible-main.yml
```
* Windows
* Enable and install WSL
* Follow the above linux steps in WSL
* Do https://stackoverflow.com/questions/58345011/setup-windows-10-workstation-using-ansible-installed-on-wsl

## You need to manually
* Install office (TODO: https://chocolatey.org/packages/office-tool#files)
* Login to Chrome, Lastpass, InoReader, Dropbox, Microsoft related products (office)
* Windows settings
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
* Voicemeeter Banana
* Setup correct file associations (for .xml, .html, etc...)
* VLC Plugins
* Audacity and configurations
* A separate packages.config for different workflows
* Add symbolic links to Dropbox bin/ folder (requires a Symlink to the Dropbox folder)
 * Move the ones that support it form the tools folder into Chocolatey
* ShareX config
* Make sure that Chrome syncs settings for refined GitHub (looks like it worked)
* Rust
* Docker (removal of old and getting new)

## TODO
* Hide excess folders I don't use anymore like 3D Objects, etc... (they're all in dropbox now)
* Add z's config (but somehow without leaking all the path names, or don't...)
* Add a little indicator to PS1 when dotfiles is out of date
* Migrate everything that needs to be into bashrc
* Finish readding paint.net and pyenv
* Better NVM management (might be nice to use a role...)