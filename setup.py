import json
import sys
import os

verifyOnly = '--verify-only' in sys.argv

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
  global verifyOnly

  isLink = os.path.islink(path)
  print(f"[{'OK' if isLink else 'NO' }]: '{path}' is {'' if isLink else 'NOT '}link ")
  if isLink or verifyOnly:
    return
  os.symlink(path, target)


#Probably requires admin...

scriptDir = os.path.dirname(sys.argv[0])
appData = os.environ["APPDATA"]
userProfile = os.environ["USERPROFILE"]

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
addSymlink(os.path.realpath(f"{scriptDir}\\sublime\\APPDATA\\Packages\\User"), f"{appData}\\Sublime Text 3\\Packages\\User")
print("Make sure to setup your Sublime license and FTP license too!")

#CONEMU
#Symlink the .xml config
addSymlink(f"{scriptDir}\\conemu\\ConEmu.xml", f"{appData}\\ConEmu.xml")
#Add our the computer default bashrc
#with open(f"{userProfile}\\.bashrc", mode="a") as fp:
#    fp.write(f"\n\nsource {scriptDir}\\cobertos.bashrc")

#Git
addSymlink(f"{scriptDir}\\git\\.gitconfig", f"{userProfile}\\.gitconfig")

#Paint.NET
addSymlink(f"{dropboxEnvDir}\\Paint.NET\\Effects", f"C:\\Program Files\\paint.net\\Effects")
addSymlink(f"{dropboxEnvDir}\\Paint.NET\\FileTypes", f"C:\\Program Files\\paint.net\\FileTypes")
addSymlink(f"{dropboxEnvDir}\\Paint.NET\\Paint.NET User Files", f"{userProfile}\\Documents\\paint.net User Files")

#Blender

#WSL (WIP)
#powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
#Restart
#powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
#powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
#~/Workspace/wsl/Ubuntu/ubuntu1804.exe