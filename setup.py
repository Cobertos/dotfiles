import json
import sys
import os
import shutil
import platform
from pathlib import Path, PurePosixPath

verifyOnly = '--verify-only' in sys.argv
environment = None
environmentOpts = list(filter(lambda s: s.startswith('--environment='), sys.argv))
if environmentOpts:
  environment = environmentOpts[-1].split('=')[-1]

#TODO: Convert to using pathlib instead of string paths in the future

def getEnvironmentFilePath(path):
  global environment
  return f"{path}##{environment}" if environment and os.path.exists(f"{path}##{environment}") else path

def appendToFile(appendString, path):
  """
  Adds string to the end of the file if the line isn't in the file already
  Make sure to add a new line yourself if you want that
  """
  global verifyOnly

  def isAppendedToFile(appendString, path):
    with open(path, mode="r") as fp:
      #Go through the entire files, but reversed to succeed fast
      for line in reversed(fp.readlines()):
        if appendString.strip() in line.strip():
          return True
    return False

  appended = isAppendedToFile(appendString, path)
  print(f"[{ 'OK' if appended else 'NO' }]: '{path}' does {'' if appended else 'NOT '}contain necessary appended line")
  if appended or verifyOnly: #already good
    return

  with open(path, mode="a") as fp:
    fp.write(appendString)

def addToPath(path):
  """Adds a path to the PATH environment variable"""
  global verifyOnly

  def isOnPath(path):
    return path in map(lambda p: p.strip(), os.environ['PATH'].split(';'))

  print(f"[{ 'OK' if isOnPath(path) else 'NO' }]: '{path}' {'' if isOnPath(path) else 'NOT '}on path ")
  if isOnPath(path) or verifyOnly: #already good
    return
  #Otherwise add it
  #os.environ["PATH"] = f"{os.environ['PATH']};{path}"
  #TODO: os.environ doesn't persist on Windows, so instead use SETX
  #TODO: This will truncate the environment variable to 1024 characters too :/
  if platform.system() == "Windows":
    os.system(f"SETX /M PATH \"%PATH%;{path}\"")
  else:
    raise NotImplementedError("AddToPath does not work on Linux variants :(")

def addSymlink(target, path):
  """Adds a symlink at the given spot"""
  #Requires admin on windows (the symlink permission)
  global verifyOnly, environment

  #Determine which target to use based on environment
  target = getEnvironmentFilePath(target)

  def isProperlyLinked(path):
    isLink = os.path.islink(path)
    if not isLink:
      return [isLink, False, '']
    
    linkResolved = Path(path).resolve()
    isLinkedProperly = os.path.normpath(str(linkResolved)) == os.path.normpath(target)
    return [isLink, isLinkedProperly, linkResolved]

  [isLink, isLinkedProperly, linkResolved] = isProperlyLinked(path)
  errStr = ('properly linked.' if isLinkedProperly else f"pointing to '{linkResolved}'.") if isLink else 'not a link.'
  print(f"[{'OK' if isLinkedProperly else 'NO' }]: '{path}' is {errStr}")
  if isLinkedProperly or verifyOnly:
    return

  #Make the link and do things if it fails
  while not isProperlyLinked(path)[1]:
    try:
      os.symlink(target, path)
    except FileExistsError as e:
      if input(f"File to symlink already exists, delete? y/N ") == 'y':
        if os.path.isfile(path):
          os.remove(path)
        elif os.path.isdir(path):
          shutil.rmtree(path)
        else:
          raise RuntimeError("Path was not a file or directory")
      else:
        return;

scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
appData = os.environ["APPDATA"]
userProfile = os.environ["USERPROFILE"]
print(scriptDir)

#TODO: Query two files and grab a json key
#dropboxInfoFile = None
#if os.path.isfile(f"{appData}\\Dropbox\\info.json"):
#    dropboxInfoFile = f"{appData}\\Dropbox\\info.json"
#elif os.path.isfile(f"{os.environ['LOCALAPPDATA']}\\Dropbox\\info.json"):
#    dropboxInfoFile = f"{os.environ['LOCALAPPDATA']}\\Dropbox\\info.json"
#with open(dropboxInfoFile) as fp:
#    dropboxEnvDir = json.load(fp)["personal"]["path"]


#SUBLIME
#Add sublime to path for `subl`
addToPath("C:\\Program Files\\Sublime Text 3")
#Make symbolic link to our Package\\User
addSymlink(f"{os.path.realpath(scriptDir)}\\sublime\\APPDATA\\Packages\\User", f"{appData}\\Sublime Text 3\\Packages\\User")
print("Make sure to setup your Sublime license and FTP license too!")

#CONEMU
#Symlink the .xml config
addSymlink(f"{scriptDir}\\conemu\\ConEmu.xml", f"{appData}\\ConEmu_190174.xml")
#Add our the computer default bashrc

#Git
addSymlink(f"{scriptDir}\\git\\.gitconfig", f"{userProfile}\\.gitconfig")
addSymlink(f"{scriptDir}\\git\\.gitignore", f"{userProfile}\\.gitignore")

#Bash
bashrcPath = getEnvironmentFilePath(f"{scriptDir}\\.bashrc")
bashrcPathPosix = Path(bashrcPath).as_posix().replace("C:", "/c")
appendToFile(f"\nsource {bashrcPathPosix}", f"{userProfile}\\.bashrc")

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

if platform.system() == "Windows" and not verifyOnly:
  #If we don't do this, then the next time we run setup.py we won't see any of the
  #system wide environment variable changes in the same shell
  os.system("refreshenv") #Will print out that it's refreshing environment variables