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
import pprint
from df.utils import getEnvironmentFilePath, getUserHome
from df.SymLinkOp import SymLinkOp
from df.RemoveFileOp import RemoveFileOp
from df.NpmInstallGlobalOp import NpmInstallGlobalOp
from df.PipInstallGlobalOp import PipInstallGlobalOp, PipXInstallGlobalOp
from df.DFOp import DFOp, DFOpLoggingFormatter
from df.AptInstallOp import AptInstallOp
from df.WriteFileOp import WriteFileOp

if platform.system() == "Windows":
  raise Exception("Nah, no Windows support anymore, too much trauma, byebye :(")

SUPPORTED_ENVIRONMENTS = [None, "desktop", "container"]
scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
userHome = getUserHome()

def bootstrap_env_desktop(opts):
  '''
  Given opts (.environment, .verify_only), runs through all the operations to
  bootstrap the machine on something that has a UI
  '''
  env = lambda p: getEnvironmentFilePath(p, opts.environment)

  # Fonts
  # TODO: Come back to this if I really end up caring again...
  # fontsPath = f"{userHome}/.local/share/fonts"
  # SymLinkOp(env(f"{os.path.realpath(scriptDir)}/fonts/Blobmoji.ttf"), f"{fontsPath}/Blobmoji.ttf")()
  # SymLinkOp(env(f"{os.path.realpath(scriptDir)}/fonts/TwitterColorEmoji-SVGinOT.ttf"), f"{fontsPath}/TwitterColorEmoji-SVGinOT.ttf")()
  # fontConfPath = f"{userHome}/.config/fontconfig"
  # SymLinkOp(env(f"{os.path.realpath(scriptDir)}/fonts/55-prefer-blobmoji-except-ripcord.conf"), f"{fontConfPath}/conf.d/55-prefer-blobmoji-except-ripcord.conf")()
  # RemoveFileOp(f"/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")() # Delete normal NotoColorEmoji font

  # Krita
  #AptInstallOp("krita",
    # Krita official PPA
  #  addRepo='ppa:kritalime/ppa')()
  kritaHomePath = f"{userHome}/.local/share/krita"
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/krita"), kritaHomePath)()

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

  # Apps
  # Some issues with this chromium being available into the future?
  # Might switch to just Chrome, cause Mint is one of the only ones that looks to have this for the forseeable future
  # https://www.zdnet.com/article/linux-distributors-frustrated-by-googles-new-chromium-web-browser-restrictions/
  AptInstallOp("chromium-browser")() # For web-dev only, don't let it be default browser
  AptInstallOp("dbeaver-ce",
    addKey="https://dbeaver.io/debs/dbeaver.gpg.key",
    addRepo="ppa:serge-rider/dbeaver-ce")()
  AptInstallOp("flameshot")()
  AptInstallOp("obs-studio",
    # OBS official PPA
    addRepo='ppa:obsproject/obs-studio')()
  AptInstallOp("seafile-gui",
    addKey='https://linux-clients.seafile.com/seafile.asc',
    addRepo='deb [arch=amd64] https://linux-clients.seafile.com/seafile-deb/focal/ stable main')()
  AptInstallOp("signal-desktop",
    addKey='https://updates.signal.org/desktop/apt/keys.asc',
    addRepo='deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main')()
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
  SymLinkOp(env(f"{scriptDir}/desktop/krita.desktop"), f"{userHome}/.local/share/applications/krita.desktop")()

  #Blender
  #TODO

def bootstrap_env_container(opts):
  pass

def bootstrap(opts):
  '''
  Given opts (.environment, .verify_only), runs through all the operations to
  bootstrap the machine
  '''
  global scriptDir, userHome

  #appData = os.environ["APPDATA"]
  env = lambda p: getEnvironmentFilePath(p, opts.environment)

  # asdf, though it was currently installed manually

  # Sublime
  # sublime-text
  AptInstallOp("apt-transport-https")() # Ensure https packages
  AptInstallOp("sublime-text",
    addKey="https://download.sublimetext.com/sublimehq-pub.gpg",
    addRepo='deb https://download.sublimetext.com/ apt/stable/')()
  sublimeConfigPath = f"{userHome}/.config/sublime-text-3/Packages/User"
  SymLinkOp(env(f"{os.path.realpath(scriptDir)}/sublime/Packages/User"), sublimeConfigPath)()

  # Sublime dependencies (for plugins)
  # NpmInstallGlobalOp("eslint_d")()
  # PipXInstallGlobalOp("yamllint")()

  # Git
  AptInstallOp("git")()
  SymLinkOp(env(f"{scriptDir}/git/.gitconfig"), f"{userHome}/.gitconfig")()
  SymLinkOp(env(f"{scriptDir}/git/.gitignore"), f"{userHome}/.gitignore")()

  # Micro
  AptInstallOp("micro")()

  # HPI/Promnesia
  #PipInstallGlobalOp("promnesia")()
  #PipInstallGlobalOp("promnesia[optional]")()
  #PipInstallGlobalOp("promnesia[markdown]")()
  #SymLinkOp(env(f"{scriptDir}/promnesia/config.py"), f"{userHome}/.config/promnesia/config.py")()
  #SymLinkOp(env(f"{scriptDir}/hpi/config"), f"{userHome}/.config/my/my/config")()

  # Bash - We generate an absolute path to the cobertos.bashrc and source it.
  # this file is what gets symlinked as .bashrc
  # TODO: Make the SymLinkOp dependent on WriteFileOp passing, maybe use a with:
  # statement or something, so that the op has to pass for the internals to run
  cobertosRCPath = os.path.abspath(scriptDir).replace("/","/")
  WriteFileOp(env(f"{scriptDir}/.bashrc"), \
f'''#AUTOGENERATED - Run bootstrap.py to regenerate
DOTFILES_ENVIRONMENT="{opts.environment}"
export DOTFILES_ENVIRONMENT
source {cobertosRCPath}/cobertos.bashrc
''')()
  SymLinkOp(f"{scriptDir}/.bashrc", f"{userHome}/.bashrc")()
  # Same with .profile
#   WriteFileOp(env(f"{scriptDir}/.profile"), \
# f'''#AUTOGENERATED - Run bootstrap.py to regenerate
# DOTFILES_ENVIRONMENT="{opts.environment}"
# export DOTFILES_ENVIRONMENT
# source {cobertosRCPath}/cobertos.profile
# ''')()
  # SymLinkOp(f"{scriptDir}/.profile", f"{userHome}/.profile")()
  # Remove .bash_profile so bash reads .profile
  RemoveFileOp(f"{userHome}/.bash_profile")

  # Npm
  # NpmInstallGlobalOp("js-yaml")()     # Tool

  # Python
  # PipXInstallGlobalOp("pylint")()

  # Misc Packages
  AptInstallOp("p7zip-full")()
  #AptInstallOp("android-sdk")() # Android platform-tools
  AptInstallOp("dbeaver-ce",
    addKey="https://dbeaver.io/debs/dbeaver.gpg.key",
    addRepo="ppa:serge-rider/dbeaver-ce")()
  AptInstallOp("dos2unix")()
  AptInstallOp("ffmpeg")() # Required for obs
  AptInstallOp("fd-find")()
  AptInstallOp("nmap")()

  #Other
  SymLinkOp(env(f"{scriptDir}/.config/yamllint/config"), f"{userHome}/.config/yamllint/config")()

  # Desktop - We only do this somewhere that has a UI
  if opts.environment == "desktop":
    bootstrap_env_desktop(opts)
  elif opts.environment == "container":
    bootstrap_env_container(opts)

def init_bootstrap(opts):
  '''
  Given opts (.environment, .verify_only), inits the bootstrapping system
  '''
  # Set verifyOnly mode globally
  DFOp.verifyOnly = opts.verify_only
  DFOp.autoAccept = opts.auto_accept

  # Verify the environment is as expected
  if opts.environment not in SUPPORTED_ENVIRONMENTS:
    raise Exception(f"Environment \"{opts.environment}\" is not a supported environment. Supported environments are {pprint.pformat(SUPPORTED_ENVIRONMENTS)}")

if __name__ == '__main__':
  # Parse all the arguments
  parser = argparse.ArgumentParser(description='Bootstraps dotfiles and my environment :3')
  parser.add_argument('--verify-only', dest='verify_only', action='store_true',
                      help='Only verify the installation, dont actually do anything')
  parser.add_argument('--yes', dest='auto_accept', action='store_true',
                      help='Performs the installation with no user acceptance')
  parser.add_argument('--environment', type=str,
                      help='a string for the environment prefix to use, uses files ending wiith ##[environment] when applicable')
  opts = parser.parse_args(sys.argv[1:])
  if opts.environment == None:
    opts.environment = os.environ["DOTFILES_ENVIRONMENT"] if "DOTFILES_ENVIRONMENT" in os.environ else None

  logger = logging.getLogger('DFOp')
  logger.setLevel(logging.DEBUG)
  formatter = DFOpLoggingFormatter('\n[%(name)20s] %(message)s')
  handler = logging.StreamHandler(sys.stdout)
  handler.terminator = ""
  handler.setFormatter(formatter)
  handler.setLevel(logging.DEBUG)
  logging.getLogger().addHandler(handler)

  print(f"=== bootstrap.py environment==\"{opts.environment}\" ===")

  init_bootstrap(opts)
  bootstrap(opts)
