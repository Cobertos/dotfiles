'''
Bootstraps the machine with my dotfiles environment
'''

import argparse
import sys
import os
import platform
import subprocess
import logging
import glob
from df.utils import getEnvironmentFilePath, getUserHome
from df.SymLinkOp import SymLinkOp
from df.RemoveFileOp import RemoveFileOp
from df.NpmInstallGlobalOp import NpmInstallGlobalOp
from df.PipInstallGlobalOp import PipInstallGlobalOp, PipXInstallGlobalOp
from df.DFOp import DFOp, DFOpLoggingFormatter
from df.AptInstallOp import AptInstallOp
from df.WriteFileOp import WriteFileOp

scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
userHome = getUserHome()

def ni():
  '''Raises NotImplementedError'''
  raise NotImplementedError

def bootstrap(opts):
  '''
  Given opts (.environment, .verify_only), runs through all the operations to
  bootstrap the machine
  '''
  global scriptDir, userHome
  #appData = os.environ["APPDATA"]
  env = lambda p: getEnvironmentFilePath(p, opts.environment)

  DFOp.verifyOnly = opts.verify_only

  # TODO:
  # Only needed on windows, in Linux we're just putting everything in .bashrc/
  # shell scripts for now...
  # AddToPath(f"{scriptDir}/onpath")()
  # asdf, though it was currently installed manually

  # Fonts
  fontsPath = f"{userHome}/.local/share/fonts" if platform.system() != "Windows" else ni()
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/fonts/Blobmoji.ttf"), f"{fontsPath}/Blobmoji.ttf")()
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/fonts/TwitterColorEmoji-SVGinOT.ttf"), f"{fontsPath}/TwitterColorEmoji-SVGinOT.ttf")()
  fontConfPath = f"{userHome}/.config/fontconfig" if platform.system() != "Windows" else ni()
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/fonts/55-prefer-blobmoji-except-ripcord.conf"), f"{fontConfPath}/conf.d/55-prefer-blobmoji-except-ripcord.conf")()
  RemoveFileOp(f"/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")() # Delete normal NotoColorEmoji font

  # Sublime
  # sublime-text
  AptInstallOp("apt-transport-https")() # Ensure https packages
  AptInstallOp("sublime-text",
    addKey="https://download.sublimetext.com/sublimehq-pub.gpg",
    addRepo='deb https://download.sublimetext.com/ apt/stable/')()
  sublimeConfigPath = f"{userHome}/.config/sublime-text-3/Packages/User" if platform.system() != "Windows" else f"{appData}/Sublime Text 3/Packages/User"
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/sublime/Packages/User"), sublimeConfigPath)()
  # sublime-merge
  AptInstallOp("sublime-merge",
    addKey="https://download.sublimetext.com/sublimehq-pub.gpg",
    addRepo='deb https://download.sublimetext.com/ apt/stable/')()
  # TODO:
  # Only needed on Windows
  # AddToPath("C:/Program Files/Sublime Text 3")() #Add sublime to path for `subl`

  # Typora
  AptInstallOp("typora",
    addKey="https://typora.io/linux/public-key.asc",
    addRepo='deb https://typora.io/linux ./')()
  typoraConfigPath = f"{userHome}/.config/Typora" if platform.system() != "Windows" else ni()
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/typora/profile.data"), f"{typoraConfigPath}/profile.data")() # Non-human readable normal settings, per Abner
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/typora/conf/conf.user.json"), f"{typoraConfigPath}/conf/conf.user.json")() # Advanced settings

  # Krita
  #AptInstallOp("krita",
    # Krita official PPA
  #  addRepo='ppa:kritalime/ppa')()
  kritaHomePath = f"{userHome}/.local/share/krita" if platform.system() != "Windows" else ni()
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/krita"), kritaHomePath)()

  # Git
  AptInstallOp("git")()
  SymLinkOp(env(f"{scriptDir}/git/.gitconfig"), f"{userHome}/.gitconfig")()
  SymLinkOp(env(f"{scriptDir}/git/.gitignore"), f"{userHome}/.gitignore")()

  # HPI/Promnesia
  #PipInstallGlobalOp("promnesia")()
  #PipInstallGlobalOp("promnesia[optional]")()
  #PipInstallGlobalOp("promnesia[markdown]")()
  #SymLinkOp(env(f"{scriptDir}/promnesia/config.py"), f"{userHome}/.config/promnesia/config.py")()
  #SymLinkOp(env(f"{scriptDir}/hpi/config"), f"{userHome}/.config/my/my/config")()

  # Firefox
  AptInstallOp("firefox")()
  firefoxConfigPathProfileMatches = glob.glob(f"{userHome}/.mozilla/firefox/*.default-release")
  if not firefoxConfigPathProfileMatches:
    print("No firefox profiles found!")
    #TODO: Maybe this should fail?
    #TODO: Maybe this should fail if more than one?
  else:
    firefoxConfigPathProfile = firefoxConfigPathProfileMatches[0]
    print(f"Firefox profile at '{firefoxConfigPathProfile}'")
    SymLinkOp(env(f"{scriptDir}/firefox/userChrome.css"), f"{firefoxConfigPathProfile}/chrome/userChrome.css")()
    SymLinkOp(env(f"{scriptDir}/firefox/user.js"), f"{firefoxConfigPathProfile}/user.js")()


  # Bash - We generate an absolute path to the cobertos.bashrc and source it.
  # this file is what gets symlinked as .bashrc
  # TODO: Make the SymLinkOp dependent on WriteFileOp passing, maybe use a with:
  # statement or something, so that the op has to pass for the internals to run
  cobertosRCPath = os.path.abspath(scriptDir).replace("/","/")
  WriteFileOp(env(f"{scriptDir}/.bashrc"), \
f'''#AUTOGENERATED - Run cli.py to regenerate
source {cobertosRCPath}/cobertos.bashrc
''')()
  SymLinkOp(f"{scriptDir}/.bashrc", f"{userHome}/.bashrc")()
  # Same with .bash_profile
  RemoveFileOp(f"{userHome}/.bash_profile") # Remove so bash reads .profile
  # Same with .profile
  WriteFileOp(env(f"{scriptDir}/.profile"), \
f'''#AUTOGENERATED - Run cli.py to regenerate
source {cobertosRCPath}/cobertos.profile
''')()
  SymLinkOp(f"{scriptDir}/.profile", f"{userHome}/.profile")()

  # Npm
  #NpmInstallGlobalOp("@vue/cli")()    # Tool
  #NpmInstallGlobalOp("serverless")()  # Tool
  NpmInstallGlobalOp("eslint_d")()    # Dependency for Sublime Linter
  NpmInstallGlobalOp("js-yaml")()     # Tool
  NpmInstallGlobalOp("lerna")()       # Tool
  # TODO:
  # Ability to use global packages in require() with NODE_PATH
  # Should work with NVM https://stackoverflow.com/a/49293370/2759427
  # AppendToEnvVar(NpmInstallGlobalOp.npmRoot(), "NODE_PATH")()

  # Python
  PipXInstallGlobalOp("yamllint")()   # Dependency for Sublime Linter
  PipXInstallGlobalOp("grip")()       # Tool - Markdown preview for GitHub
  PipXInstallGlobalOp("pipenv")()
  PipXInstallGlobalOp("pylint")()
  #PipXInstallGlobalOp("awscli")()

  # PipInstallGlobal("pyenv-win")("--target", f"{userHome}/.pyenv") #This package is annoying...
  # #From https://github.com/pyenv-win/pyenv-win#finish-the-installation
  # SetEnvVar(f"{userHome}/.pyenv/pyenv-win", "PYENV")()
  # AddToPath("%PYENV%/bin", prepend=True)() #Needs to come before WindowsApps, cause Python is in there by default now?
  # AddToPath("%PYENV%/shims", prepend=True)()
  # #print("Run pyenv rehash to get this to work...")

  # Misc Packages
  # TODO: Ripcord, only provides an AppImage
  AptInstallOp("p7zip-full")()
  #AptInstallOp("android-sdk")() # Android platform-tools
  # Some issues with this chromium being available into the future?
  # Might switch to just Chrome, cause Mint is one of the only ones that looks to have this for the forseeable future
  # https://www.zdnet.com/article/linux-distributors-frustrated-by-googles-new-chromium-web-browser-restrictions/
  AptInstallOp("chromium-browser")() # For web-dev only, don't let it be default browser
  AptInstallOp("dbeaver-ce",
    addKey="https://dbeaver.io/debs/dbeaver.gpg.key",
    addRepo="ppa:serge-rider/dbeaver-ce")()
  AptInstallOp("discord",
    debUrl="https://discord.com/api/download?platform=linux&format=deb")()
  AptInstallOp("dos2unix")()
  AptInstallOp("ffmpeg")() # Required for obs
  AptInstallOp("flameshot")()
  AptInstallOp("insomnia",
    addKey="https://insomnia.rest/keys/debian-public.key.asc",
    addRepo="deb [trusted=yes arch=amd64] https://download.konghq.com/insomnia-ubuntu/ default all")()
  AptInstallOp("nmap")()
  AptInstallOp("obs-studio",
    # OBS official PPA
    addRepo='ppa:obsproject/obs-studio')()
  AptInstallOp("seafile-gui",
    addKey='https://linux-clients.seafile.com/seafile.asc',
    addRepo='deb [arch=amd64] https://linux-clients.seafile.com/seafile-deb/focal/ stable main')()
  AptInstallOp("slack-desktop",
    debUrl="https://downloads.slack-edge.com/linux_releases/slack-desktop-4.12.2-amd64.deb")() #TODO: Find a latest deb, if Slack provides it
  AptInstallOp("signal-desktop",
    addKey='https://updates.signal.org/desktop/apt/keys.asc',
    addRepo='deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main')()
  AptInstallOp("spotify-client",
    addKey='https://download.spotify.com/debian/pubkey_0D811D58.gpg',
    addRepo='deb http://repository.spotify.com stable non-free')()
  AptInstallOp("sqlitebrowser",
    # PPA maintained by https://github.com/deepsidhu1313
    # though the docs officially mention it as existing
    addRepo='ppa:linuxgndu/sqlitebrowser')()
  AptInstallOp("vlc")()
  AptInstallOp("xclip")()
  # TODO: Package manager is 0.6.0, and I'd prefer to get 0.7.1 (master) rn...
  # AptInstallOp("zig",
  #   addKey='https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x379ce192d401ab61',
  #   addRepo='deb https://dl.bintray.com/dryzig/zig-ubuntu focal main')()

  #Desktop Files
  SymLinkOp(env(f"{scriptDir}/desktop/obsidian.desktop"), f"{userHome}/.local/share/applications/obsidian.desktop")()


  #Other
  SymLinkOp(env(f"{scriptDir}/.vuerc"), f"{userHome}/.vuerc")()
  SymLinkOp(env(f"{scriptDir}/.config/yamllint/config"), f"{userHome}/.config/yamllint/config")()

  #Blender
  #TODO

if __name__ == '__main__':
  # Parse all the arguments
  parser = argparse.ArgumentParser(description='Bootstraps dotfiles and my environment :3')
  parser.add_argument('--verify-only', dest='verify_only', action='store_true',
                      help='Only verify the installation, dont actually do anything')
  parser.add_argument('--environment', type=str,
                      help='a string for the environment prefix to use, uses files ending wiith ##[environment] when applicable')
  opts = parser.parse_args(sys.argv[1:])

  logger = logging.getLogger('DFOp')
  logger.setLevel(logging.DEBUG)
  formatter = DFOpLoggingFormatter('\n[%(name)20s] %(message)s')
  handler = logging.StreamHandler(sys.stdout)
  handler.terminator = ""
  handler.setFormatter(formatter)
  handler.setLevel(logging.DEBUG)
  logging.getLogger().addHandler(handler)

  bootstrap(opts)

  # Refresh the environment after running if Windows
  if platform.system() == "Windows" and not opts.verify_only:
    #If we don't do this, then the next time we run setup.py we won't see any of the
    #system wide environment variable changes in the same shell
    subprocess.run([f"{scriptDir}/onpath/refreshenv.cmd"], check=True) #Will print out that it's refreshing environment variables
