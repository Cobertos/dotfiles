import json
import sys
import os
from pathlib import Path

verifyOnly = '--verify-only' in sys.argv
environment = None
environmentOpts = list(filter(lambda s: s.startswith('--environment='), sys.argv))
if environmentOpts:
  environment = environmentOpts[-1].split('=')[-1]

def addToPath(path):
  """Adds a path to the PATH environment variable"""
  global verifyOnly

  isOnPath = path in map(lambda p: p.strip(), os.environ['PATH'].split(';'))
  print(f"[{ 'OK' if isOnPath else 'NO' }]: '{path}' {'' if isOnPath else 'NOT '}on path ")
  if isOnPath or verifyOnly: #already good
    return
  #Otherwise add it
  os.environ["PATH"] = f"{os.environ['PATH']};{path}"

def addSymlink(target, path):
  """Adds a symlink at the given spot"""
  #Requires admin on windows (the symlink permission)
  global verifyOnly, environment

  #Determine which target to use based on environment
  if environment and os.path.isfile(f"{target}##{environment}"):
    target = f"{target}##{environment}"

  isLinkedProperly = False
  isLink = os.path.islink(path)
  if isLink:
    linkResolved = Path(path).resolve()
    isLinkedProperly = os.path.normpath(str(linkResolved)) == os.path.normpath(target)

  errStr = ('properly linked.' if isLinkedProperly else f"pointing to '{linkResolved}'.") if isLink else 'not a link.'
  print(f"[{'OK' if isLinkedProperly else 'NO' }]: '{path}' is {errStr}")
  if isLinkedProperly or verifyOnly:
    return

  os.symlink(target, path)

scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
appData = os.environ["APPDATA"]
userProfile = os.environ["USERPROFILE"]
print(scriptDir)

#TODO: Query two files and grab a json key
if os.path.isfile(f"{appData}\\Dropbox\\info.json"):
    dropboxInfoFile = f"{appData}\\Dropbox\\info.json"
elif os.path.isfile(f"{os.environ['LOCALAPPDATA']}\\Dropbox\\info.json"):
    dropboxInfoFile = f"{os.environ['LOCALAPPDATA']}\\Dropbox\\info.json"
with open(dropboxInfoFile) as fp:
    dropboxEnvDir = json.load(fp)["personal"]["path"]


#SUBLIME
#Add sublime to path for `subl`
addToPath("C:\\Program Files\\Sublime Text 3")
#Make symbolic link to our Package\\User
addSymlink(f"{os.path.realpath(scriptDir)}\\sublime\\APPDATA\\Packages\\User", f"{appData}\\Sublime Text 3\\Packages\\User")
print("Make sure to setup your Sublime license and FTP license too!")

#CONEMU
#Symlink the .xml config
#addSymlink(f"{scriptDir}\\conemu\\ConEmu.xml", f"{appData}\\ConEmu.xml")
#Add our the computer default bashrc
#with open(f"{userProfile}\\.bashrc", mode="a") as fp:
#    fp.write(f"\n\nsource {scriptDir}\\cobertos.bashrc")

#Git
addSymlink(f"{scriptDir}\\git\\.gitconfig", f"{userProfile}\\.gitconfig")
addSymlink(f"{scriptDir}\\git\\.gitignore", f"{userProfile}\\.gitignore")

#Paint.NET
#addSymlink(f"{dropboxEnvDir}\\Paint.NET\\Effects", f"C:\\Program Files\\paint.net\\Effects")
#addSymlink(f"{dropboxEnvDir}\\Paint.NET\\FileTypes", f"C:\\Program Files\\paint.net\\FileTypes")
#addSymlink(f"{dropboxEnvDir}\\Paint.NET\\Paint.NET User Files", f"{userProfile}\\Documents\\paint.net User Files")

#Blender

#WSL (WIP)
#powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
#Restart
#powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
#powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
#~/Workspace/wsl/Ubuntu/ubuntu1804.exe