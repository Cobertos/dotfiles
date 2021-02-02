# Dot Files

A collection of configs and dot files I use

* **Cross Platform** - Meant to work on Linux _and_ Windows
* **All Use Cases** - All configs have defaults, though special configs with suffix `##XXX` can be chosen with priority using `--environment=XXX` flag
* **Linking** - Symlinks over copying
* **Public** - Private keys and licenses are separate (for now... keeping an eye on git-crypt)
* **Automatic** - `python bootstrap.py` sets up everything. `--verify-only` only verifies, and is run every time I open a terminal

Supports:
* A bunch of stuff, though [`bootstrap.py`](/bootstrap.py) gives the best overview.

## Installation
### Linux Installation
```bash
cd ~
sudo apt update && sudo apt install git
git clone https://github.com/Cobertos/dotfiles.git
cd dotfiles
python3 bootstrap.py # Make sure to use the right --environment=XXX
```

### Windows (WSL) Installation
* Enable and install WSL
* Follow the above Linux steps in WSL (might need to manually install Python too)

### Windows Native Installation (old, might not work)
* [Install chocolatey](https://chocolatey.org/docs/installation)
 * I would like to automate this but there's a lot of overhead with Python)
* `choco install ./packages.config`
* Install `pyenv` by downloading and extracting at the correct location and setting up variables
* Install Python 3.6+
* `python bootstrap.py`
 * Make sure to use the right `--environment=XXX`!

## Installation Part 2 (everything that I have yet to automate)
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
 * Download playlists
* Install Unity-Hub (broken on Chocolatey)
* Blender is installed separately (managing multiple Blender versions)
* Setup OBS to record into Seafile (save these prefs)
* Setup Unity defaults (External editor and stuff) (would be nice to capture these prefs)
* Hide excess folders in explorer/nemo, like Picture, Videos, etc
* Docker (removal of old and getting new)
* Configure Typora

### Linux specific manually
* Configure Linux Mint Desktop
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
* ConEmu
 * Setup conemu here manually
 * TODO: Re-evaluate even using ConEmu, Windows terminal new is fine

## Future Support
* Voicemeeter Banana
* Setup correct file associations (for .xml, .html, etc...)
* VLC Plugins
* Audacity and configurations
* A separate packages.config for different workflows
* ShareX config
* Installing chocolatey packages
* Make sure that Chrome/Firefox syncs settings for refined GitHub (looks like it worked)
* Rust
* Readd all the windows registry, theme stuff, and paint.NET
  * The ansible branch had some extras for screen rotation disable and removing Python execution aliases on Windows
  * The ansible branch also solves choco git install flags better, and by default asks for WSL to be installed (which IMO is smarter)
* /etc/hosts and C:\Windows\System32\drivers\etc\hosts or wherever it is in Windows
* Seafile notifications disabling?
* Windows PowerTools?
* nvm, pyenv

### Won't Support
* Pulling in z's config, as it should honeslty be separate per-machine, due to file path differences, and it can contain things I don't want public

## TODO
* Add a little indicator to PS1 when dotfiles is out of date
* Yamllint isnt installed but it says it is
* Consider removing WavesMaxxAudio to stop popup and background processing
 * https://github.com/GrzegorzKozub/xps
 * https://github.com/kevinshroff/KSMRD-Modded-Realtek-Audio-Drivers
* Consider applying filter keys faster repeats fix
 * https://superuser.com/questions/1058474/increase-keyboard-repeat-rate-beyond-control-panel-limits-in-windows-10
 * This seems to be a Windows 10/Dell Latitude issue. I dont have this issue on this computer in Linux Mint...
* Disable Intel AMT