import argparse
import sys
import os
import platform
import subprocess
from functools import partial
from utils import getDropboxDir
from BootstrapOperations import AddToPath, AddSymLink, NpmInstallGlobal, \
  PipInstallGlobal, AppendToEnvVar, SetEnvVar, BootstrapOpRunner

LOG_RED = lambda s: f"\033[38;5;1m{s}\033[0m"
LOG_GREEN = lambda s: f"\033[38;5;2m{s}\033[0m"
LOG_YELLOW = lambda s: f"\033[38;5;3m{s}\033[0m"
LOG_LEFT = "\033[D"

#Overwrite print to always flush
print = partial(print, flush=True)
printnln = partial(print, end='')

scriptDir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

def bootstrap(**opts):
  global scriptDir
  appData = os.environ["APPDATA"]
  userProfile = os.environ["USERPROFILE"]
  dropboxDir = getDropboxDir()

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
          if op.verify_only: #Only verifying, don't continue to execute
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
    AddToPath(f"{scriptDir}\\onpath", **opts)()

    #SUBLIME
    AddToPath("C:\\Program Files\\Sublime Text 3", **opts)() #Add sublime to path for `subl`
    #Make symbolic link to our Package\\User
    AddSymLink(f"{os.path.realpath(scriptDir)}\\sublime\\APPDATA\\Packages\\User", f"{appData}\\Sublime Text 3\\Packages\\User", **opts)()

    #CONEMU
    #Symlink the .xml config
    AddSymLink(f"{scriptDir}\\conemu\\ConEmu_190714.xml", f"{appData}\\ConEmu.xml", **opts)()

    #Git
    AddSymLink(f"{scriptDir}\\git\\.gitconfig", f"{userProfile}\\.gitconfig", **opts)()
    AddSymLink(f"{scriptDir}\\git\\.gitignore", f"{userProfile}\\.gitignore", **opts)()

    #Bash
    AddSymLink(f"{scriptDir}\\.bashrc", f"{userProfile}\\.bashrc", **opts)()

    #Npm
    #Ability to use global packages in require() with NODE_PATH
    #Should work with NVM https://stackoverflow.com/a/49293370/2759427
    AppendToEnvVar(NpmInstallGlobal.npmRoot(), "NODE_PATH", **opts)()
    NpmInstallGlobal("@vue/cli", **opts)()   #CLI tool
    NpmInstallGlobal("serverless", **opts)() #CLI tool
    NpmInstallGlobal("eslint_d", **opts)()   #Sublime Text Plugin Dependency
    NpmInstallGlobal("lessmd", **opts)()     #CLI utility to preview Markdown
    NpmInstallGlobal("js-yaml", **opts)()    #Useful tool

    #Python
    PipInstallGlobal("yamllint", **opts)()
    PipInstallGlobal("pyenv-win", **opts)("--target", f"{userProfile}\\.pyenv") #This package is annoying...
    #From https://github.com/pyenv-win/pyenv-win#finish-the-installation
    SetEnvVar(f"{userProfile}\\.pyenv\\pyenv-win", "PYENV", **opts)()
    AddToPath("%PYENV%\\bin", prepend=True, **opts)() #Needs to come before WindowsApps, cause Python is in there by default now?
    AddToPath("%PYENV%\\shims", prepend=True, **opts)()
    #print("Run pyenv rehash to get this to work...")

    #Other
    AddSymLink(f"{scriptDir}\\.vuerc", f"{userProfile}\\.vuerc", **opts)()
    AddSymLink(f"{scriptDir}\\.config\\yamllint\\config", f"{userProfile}\\.config\\yamllint\\config", **opts)()

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
  opts = vars(parser.parse_args(sys.argv[1:]))

  bootstrap(**opts)

  # Refresh the environment after running if Windows
  if platform.system() == "Windows" and not opts['verify_only']:
    #If we don't do this, then the next time we run setup.py we won't see any of the
    #system wide environment variable changes in the same shell
    subprocess.run([f"{scriptDir}\\onpath\\refreshenv.cmd"]) #Will print out that it's refreshing environment variables