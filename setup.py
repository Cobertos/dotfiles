#Probably requires admin...

scriptDir = os.path.dirname(sys.argv[0])
appData = os.environ["APPDATA"]
userProfile = os.environ["USERPROFILE"]

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


#WSL (WIP)
#powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
#Restart
#powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
#powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
#~/Workspace/wsl/Ubuntu/ubuntu1804.exe