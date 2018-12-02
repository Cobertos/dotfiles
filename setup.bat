::Requires ADMIN

::SUBLIME
::Add sublime to path for `subl`
SETX /M PATH "%PATH%;C:\Program Files\Sublime Text 3"
XCOPY /F /Y /E .\sublime "%APPDATA%\Sublime Text 3\Packages\User"
::setup license
::setup SFTP license

::CONEMU
MKLINK %APPDATA%\ConEmu.xml %~dp0\conemu\ConEmu.xml
SET BashrcFile=%UserProfile%\.bashrc
::Substitute \ for /
SET BashrcTarget=%~dp0\cobertos.bashrc
SET BashrcTarget=%BashrcTarget:\=/%
::Print two newlines and then `source %BashrcTarget%`
ECHO. >> %BashrcFile%
ECHO. >> %BashrcFile%
ECHO. source %BashrcTarget% >> %BashrcFile%

::Git
MKLINK %UserProfile%\.gitconfig %~dp0\git\.gitconfig

::WSL (WIP)
powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
::Restart
powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
~/Workspace/wsl/Ubuntu/ubuntu1804.exe