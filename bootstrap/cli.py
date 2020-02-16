import argparse
import sys
import os
import platform
import subprocess
import logging
from functools import partial
import winreg
from utils import getDropboxDir, getEnvironmentFilePath
from BootstrapOperations import AddToPath, AddSymLink, NpmInstallGlobal, \
  PipInstallGlobal, AppendToEnvVar, SetEnvVar, SetRegKey, SetTheme, BootstrapOpRunner

LOG_RED = lambda s: f"\033[38;5;1m{s}\033[0m"
LOG_GREEN = lambda s: f"\033[38;5;2m{s}\033[0m"
LOG_YELLOW = lambda s: f"\033[38;5;3m{s}\033[0m"
LOG_LEFT = "\033[D"

#Overwrite print to always flush
print = partial(print, flush=True)
printnln = partial(print, end='')

scriptDir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

def bootstrap(opts):
  global scriptDir
  appData = os.environ["APPDATA"]
  localAppData = os.environ["LOCALAPPDATA"]
  userProfile = os.environ["USERPROFILE"]
  dropboxDir = getDropboxDir()
  env = lambda p: getEnvironmentFilePath(p, opts.environment)

  class BootstrapLoggingOpRunner(BootstrapOpRunner):
    def handleOp(self, op, *args, **kwargs):
      desc = op.description()
      printnln(f"[    ] {desc}")

      try:
        test = op.test()
        if test: #Did the test pass, is the Op already implemented?
          print(f"\r[{LOG_GREEN('NOOP')}] {desc}")
          return # Already done
        else:
          printnln(f"\r[{LOG_YELLOW('TODO')}] {desc}")
          if opts.verify_only: #Only verifying, don't continue to execute
            print()
            return
      except Exception as e:
        test = False
        print(f"\r[{LOG_RED('FAIL')}] {desc}")
        print(e)
        return

      op.execute(*args, **kwargs)
      print(f"\r[{LOG_GREEN(' OK ')}] {desc}")

  with BootstrapLoggingOpRunner():
    AddToPath(f"{scriptDir}\\onpath")()

    #SUBLIME
    AddToPath("C:\\Program Files\\Sublime Text 3")() #Add sublime to path for `subl`
    #Make symbolic link to our Package\\User
    AddSymLink(env(f"{os.path.realpath(scriptDir)}\\sublime\\APPDATA\\Packages\\User"), f"{appData}\\Sublime Text 3\\Packages\\User")()

    #CONEMU
    #Symlink the .xml config
    AddSymLink(env(f"{scriptDir}\\conemu\\ConEmu_191012.xml"), f"{appData}\\ConEmu.xml")()

    #Git
    AddSymLink(env(f"{scriptDir}\\git\\.gitconfig"), f"{userProfile}\\.gitconfig")()
    AddSymLink(env(f"{scriptDir}\\git\\.gitignore"), f"{userProfile}\\.gitignore")()

    #Bash
    AddSymLink(env(f"{scriptDir}\\.bashrc"), f"{userProfile}\\.bashrc")()

    #Npm
    #Ability to use global packages in require() with NODE_PATH
    #Should work with NVM https://stackoverflow.com/a/49293370/2759427
    AppendToEnvVar(NpmInstallGlobal.npmRoot(), "NODE_PATH")()
    NpmInstallGlobal("@vue/cli")()   #CLI tool
    NpmInstallGlobal("serverless")() #CLI tool
    NpmInstallGlobal("eslint_d")()   #Sublime Text Plugin Dependency
    NpmInstallGlobal("lessmd")()     #CLI utility to preview Markdown
    NpmInstallGlobal("js-yaml")()    #Useful tool

    #Python
    PipInstallGlobal("yamllint")()
    PipInstallGlobal("pyenv-win")("--target", f"{userProfile}\\.pyenv") #This package is annoying...
    #From https://github.com/pyenv-win/pyenv-win#finish-the-installation
    SetEnvVar(f"{userProfile}\\.pyenv\\pyenv-win", "PYENV")()
    AddToPath("%PYENV%\\bin", prepend=True)() #Needs to come before WindowsApps, cause Python is in there by default now?
    AddToPath("%PYENV%\\shims", prepend=True)()
    #print("Run pyenv rehash to get this to work...")

    #Other
    AddSymLink(env(f"{scriptDir}\\.vuerc"), f"{userProfile}\\.vuerc")()
    AddSymLink(env(f"{scriptDir}\\.config\\yamllint\\config"), f"{userProfile}\\.config\\yamllint\\config")()

    #Paint.NET - Supports Windows store version
    paintNetWindowsStore = bool(subprocess.check_output("powershell -Command \"Get-AppxPackage -Name dotPDNLLC.paint.net\""))
    paintNetProgramFiles = bool(os.path.exists("C:\\Program Files\\paint.net\\Effects")) #Shitty test but what you gonna do...
    paintNetInstalled = paintNetWindowsStore or paintNetProgramFiles
    print(f"Paint.NET is {'' if paintNetInstalled else 'NOT '}installed")
    if paintNetInstalled:
      paintNetDataDir = (
        #Windows store requires the creation of a folder in Documents
        #https://forums.getpaint.net/topic/112007-windows-store-version-and-plugins/
        f"{userProfile}\\Documents\\paint.net App Files" if paintNetWindowsStore else 
        #Otherwise use the default program files directory that it normally installs into
        f"C:\\Program Files\\paint.net")

      #if paintNetWindowsStore:
      #  ensureDirectory(paintNetDataDir)

      #addSymlink(f"{dropboxDir}\\Environment\\Paint.NET\\Effects", f"{paintNetDataDir}\\Effects")
      #addSymlink(f"{dropboxDir}\\Environment\\Paint.NET\\FileTypes", f"{paintNetDataDir}\\FileTypes")
      #addSymlink(f"{dropboxDir}\\Environment\\Paint.NET\\Paint.NET User Files", f"{userProfile}\\Documents\\paint.net User Files")

    # == WINDOWS ==
    #Set the communication ducking to 'Do Nothing'
    SetRegKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Multimedia\\Audio', \
      'UserDuckingPreference', winreg.REG_DWORD, 3)() #Default is key not present
    #https://gist.github.com/NickCraver/7ebf9efbfd0c3eab72e9
    #TODO: Add more from here...
    #Privacy related
    # Disable "Allow advertisers to use my advertising ID", default 1
    SetRegKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo', \
      'Enabled', winreg.REG_DWORD, 0)()
    # WiFi sense shares the password for the WiFi with contacts in Outlook, Skype, etc (wtf...?)
    # WiFi Sense: HotSpot Sharing: Disable, default 1
    SetRegKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\PolicyManager\\default\\WiFi\\AllowWiFiHotSpotReporting', \
      'value', winreg.REG_DWORD, 0)()
    # WiFi Sense: Shared HotSpot Auto-Connect: Disable, default 1
    SetRegKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\PolicyManager\\default\\WiFi\\AllowAutoConnectToWiFiSenseHotspots', \
      'value', winreg.REG_DWORD, 0)()
    # Disable Bing search results, rewards, etc in search, all really annoying default 1
    SetRegKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Search', \
      'BingSearchEnabled', winreg.REG_DWORD, 0)()
    #Activity sharing
    SetRegKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Policies\\Microsoft\\Windows\\System', \
      'EnableActivityFeed', winreg.REG_DWORD, 0)()
    SetRegKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Policies\\Microsoft\\Windows\\System', \
      'PublishUserActivities', winreg.REG_DWORD, 0)()
    SetRegKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Policies\\Microsoft\\Windows\\System', \
      'UploadUserActivities', winreg.REG_DWORD, 0)()
    #Functionality related
    #Explorer launch to "This PC" (1) instead of default "Quick Access" (2)
    SetRegKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', \
      'LaunchTo', winreg.REG_DWORD, 1)()
    #Theme personanlization - Use .theme file for ease without a ton of reg editting
    #You can also sync it if you're using the same Windows account
    #https://docs.microsoft.com/en-us/windows/win32/controls/themesfileformat-overview#slideshow-section
    #%LOCALAPPDATA%\Microsoft\Windows\Themes\
    SetTheme(env(f"{scriptDir}\\cobertos.theme"))()

  #Blender

  #WSL (WIP)
  #powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
  #Restart
  #powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
  #powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
  #~/Workspace/wsl/Ubuntu/ubuntu1804.exe

if __name__ == '__main__':
  # Parse all the arguments
  parser = argparse.ArgumentParser(description='Bootstraps dotfiles and my environment :3')
  parser.add_argument('--verify-only', dest='verify_only', action='store_true',
                      help='Only verify the installation, dont actually do anything')
  parser.add_argument('--environment', type=str,
                      help='a string for the environment prefix to use, uses files ending wiith ##[environment] when applicable')
  opts = parser.parse_args(sys.argv[1:])

  logger = logging.getLogger('BootstrapOperation')
  logger.setLevel(logging.DEBUG)
  # class CustomFormatter(logging.Formatter):
  #     def format(self, record):
  #         title = record.title if hasattr(record, 'title') else ""
  #         return f'[{record.process}] "{title[:20].ljust(20)}": {record.getMessage()}'
  formatter = logging.Formatter('\n[%(name)20s] %(message)s') #%(levelname)s %(asctime)s - %(name)s - 
  handler = logging.StreamHandler(sys.stdout)
  handler.setFormatter(formatter)
  handler.setLevel(logging.DEBUG)
  logging.getLogger().addHandler(handler)

  bootstrap(opts)

  # Refresh the environment after running if Windows
  if platform.system() == "Windows" and not opts.verify_only:
    #If we don't do this, then the next time we run setup.py we won't see any of the
    #system wide environment variable changes in the same shell
    subprocess.run([f"{scriptDir}\\onpath\\refreshenv.cmd"]) #Will print out that it's refreshing environment variables