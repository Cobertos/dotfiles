# Dot Files

My collection of dotfiles + a [bootstrapping](./bootstrap.py) script

* **Cross Platform** - Meant to work on Linux (Mint) _and_ Windows
* **Linking** - Symlinks over copying
* **Public** - Private keys and licenses are separate (for now... keeping an eye on git-crypt)
* **Automatic** - `python bootstrap.py` sets up everything. `--verify-only` only verifies, and is run every time I open a terminal
* **Multi-environment** - All configs have defaults, though special configs with suffix `##XXX` can be chosen with priority using `--environment=XXX` flag

<p align="center">
  <img alt="sample output of dotfiles verification" src="./meta/dotfiles-verify.png">
</p>

Supports:

<p align="justify">
  <img alt="git" src="./meta/git-logo-75h.png">
  <img alt="sublime text" src="./meta/sublime-logo-75h.png">
  <img alt="typora" src="./meta/typora-logo-75h.png">
</p>

as well as [asdf](https://github.com/asdf-vm/asdf), [Z](https://github.com/rupa/z), [flameshot](https://flameshot.org/), [Discord](https://discord.com), [ffmpeg](https://ffmpeg.org/), [Insomnia](https://insomnia.rest/), [Krita](https://krita.org/en/), [OBS](https://obsproject.com/), [Seafile](https://www.seafile.com/en/home/), and a ton more,,,

## Installation
### Linux Installation
```bash
cd ~
sudo apt update && sudo apt install git
git clone https://github.com/Cobertos/dotfiles.git
cd dotfiles
python3 bootstrap.py # Make sure to use the right --environment=XXX

# TODO: Might need to manually install asdf first to get a python version, but
# you have to run this anyway after installing asdf to get the version managers
# python3 came with my system which at least allowed me to bootstrap my stuff
asdf plugin add python
python3 bootstrap.py
```

### Windows (WSL) Installation (untested, ;w;)
* Enable and install WSL
* Follow the above Linux steps in WSL (might need to manually install Python too)

### Windows Native Installation using Git Bash (old, might not work)
(TODO: This is super old, no idea if asdf will work with windows git bash)
(TODO: This definitely might break in Windows because all the paths got changed from \\ to /)
* [Install chocolatey](https://chocolatey.org/docs/installation)
  * I would like to automate this but there's a lot of overhead with Python)
* `choco install ./packages.config`
* Install `pyenv` by downloading and extracting at the correct location and setting up variables
* Install Python 3.6+
* `python bootstrap.py`
  * Make sure to use the right `--environment=XXX`!
* You will need to manually install nvm for Windows for nodejs stuff

## Installation Part 2 (everything that I have yet to automate)
* asdf installation complications
  * `asdf plugin add python && asdf plugin add nodejs`
  * Nodejs
  * https://github.com/asdf-vm/asdf-nodejs
  * `bash -c '${ASDF_DATA_DIR:=$HOME/.asdf}/plugins/nodejs/bin/import-release-team-keyring'`
  * `asdf reshim` after installs that update whats on the path
  * Python
  * https://github.com/danhper/asdf-python
  * https://github.com/pyenv/pyenv/wiki/Common-build-problems
  * `sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git`
* Install Firefox
  * Login to Firefox
  * Disable DNS over HTTPS (or figure out a way to get hosts file working without it)
  * Setup the search engine aliases for `@google` and switch from Yahoo to DDG
  * Login to InoReader
  * Login to Mangools
  * Migrate any Tampermonkey scripts
* Sublime
  * Install package control to recognize symlinked packages
  * Install license and license for FTP
  * Setup TabNine (TabNine::Config then paste key for TabNine Local)
* Spotify
  * Toggle download playlists
* Install Unity Hub
* Blender is installed separately (managing multiple Blender versions)
* Setup OBS to record into Seafile (save these prefs)
* Setup Unity defaults (External editor and stuff) (would be nice to capture these prefs)
* Hide excess folders in explorer/nemo, like Picture, Videos, etc
* Docker (removal of old and getting new)
* Configure Typora settings
* Configure fonts
  * Just install the Twemoji font, or Blobmoji if RipCord ever supports it/unless we can pass Twemoji to just RipCord and use Blobmoji elsewhere?
  * https://dev.cancel.fm/tktview?name=acaddd470e
  * https://wiki.archlinux.org/index.php/font_configuration#Force_emoji_font

### Linux specific manually
* Configure Linux Mint Desktop
  * Change the theme to Dark (for Window borders, controls, and desktop)
  * Change wallpapers/backgrouns to the folder that has them all in it
  * Add a panel to every monitor, without grouped list applet merging and with window titles
  * Change the Linux Mint start menu icon
* Install NVIDIA and eGPU drivers and all the work that goes into that

### Windows specific manually
* Windows settings
  * Lockscreen picture
  * Uninstall unwanted default apps
  * Connect phone to My Phone
  * Login to other Microsoft related products (Office)
  * Install office
  * Set surface pen pressure to like 8-9?
  * Configure taskbar preferences (non grouping etc)
  * Remove certain pins from the taskbar
  * Make backspace faster/proper speed
  * Remove OneDrive
  * Rename computer
  * Install Windows App Store apps (including Paint.NET and Spotify)

## Future Support
* Voicemeeter Banana (Linux / Ubuntu equivalent?)
* Setup correct file associations (for .xml, .html, etc...)
* VLC Plugins
* Audacity and configurations
* Make sure that Chrome/Firefox syncs settings for refined GitHub (looks like it worked)
* /etc/hosts and C:\Windows\System32\drivers\etc\hosts or wherever it is in Windows
* Seafile notifications disabling?
* Configure keybindings (like for flameshot)
* Add a little indicator to PS1 when dotfiles is out of date

### Won't Support
* Pulling in z's config, as it should honeslty be separate per-machine, due to file path differences, and it can contain things I don't want public

## Windows TODOs
* Re-evaluate if ConEmu needs to be used at all
* Installing chocolatey packages
* A separate packages.config for different workflows
* Readd all the windows registry, theme stuff, and paint.NET
  * The ansible branch had some extras for screen rotation disable and removing Python execution aliases on Windows
  * The ansible branch also solves choco git install flags better, and by default asks for WSL to be installed (which IMO is smarter)
* Windows PowerTools?
* Consider removing WavesMaxxAudio to stop popup and background processing
  * https://github.com/GrzegorzKozub/xps
  * https://github.com/kevinshroff/KSMRD-Modded-Realtek-Audio-Drivers
* Consider applying filter keys faster repeats fix
  * https://superuser.com/questions/1058474/increase-keyboard-repeat-rate-beyond-control-panel-limits-in-windows-10
  * This seems to be a Windows 10/Dell Latitude issue. I dont have this issue on this computer in Linux Mint...
* Disable Intel AMT