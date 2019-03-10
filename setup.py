import json

#Probably requires admin...

scriptDir = os.path.dirname(sys.argv[0])
appData = os.environ["APPDATA"]
userProfile = os.environ["USERPROFILE"]

#TODO: Query two files and grab a json key
if os.path.isfile(f"{appData}\\Dropbox\\info.json"):
    dropboxInfoFile = f"{appData}\\Dropbox\\info.json"
else if os.path.isfile(f"{os.environ["LOCALAPPDATA"]}\\Dropbox\\info.json"):
    dropboxInfoFile = f"{os.environ["LOCALAPPDATA"]}\\Dropbox\\info.json"
with open(dropboxInfoFile) as fp:
    dropboxEnvDir = json.load(fp)["personal"]["path"]


#SUBLIME
#Add sublime to path for `subl`
os.environ["PATH"] = f"{os.environ["PATH"]};C:\\Program Files\\Sublime Text 3"
#Make symbolic link to our Package\\User
os.symlink(os.path.realpath(f"{scriptDir}\\sublime\\APPDATA\\Packages\\User"), 
  f"{appData}\\Sublime Text 3\\Packages\\User")
print("Make sure to setup your Sublime license and FTP license too!")

#CONEMU
#Symlink the .xml config
os.symlink(f"{scriptDir}\\conemu\\ConEmu.xml", f"{appData}\\ConEmu.xml")
#Add our the computer default bashrc
with open(f"{userProfile}\\.bashrc", mode="a") as fp:
    fp.write(f"\n\nsource {scriptDir}\\cobertos.bashrc")

#Git
os.symlink(f"{scriptDir}\\git\\.gitconfig", f"{userProfile}\\.gitconfig")

#Paint.NET
os.symlink(f"{dropboxEnvDir}\\Paint.NET\\Effects", f"C:\\Program Files\\paint.net\\Effects")
os.symlink(f"{dropboxEnvDir}\\Paint.NET\\FileTypes", f"C:\\Program Files\\paint.net\\FileTypes")
os.symlink(f"{dropboxEnvDir}\\Paint.NET\\Paint.NET User Files", f"{userProfile}\\Documents\\paint.net User Files")

#Blender

#WSL (WIP)
#powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
#Restart
#powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
#powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
#~/Workspace/wsl/Ubuntu/ubuntu1804.exe