::Requires ADMIN

::SUBLIME
::Add sublime to path for `subl`
SETX /M PATH "%PATH%;C:\Program Files\Sublime Text 3"
XCOPY /F /Y /E .\sublime "%APPDATA%\Sublime Text 3\Packages\User"
::setup license
::setup SFTP license

::CONEMU
XCOPY /F /Y .\conemu\ConEmu.xml %APPDATA%\ConEmu.xml
ECHO. "\r\n\r\nsource %~dp0\cobertos.bashrc" >> %UserProfile%\.bashrc

::WSL
powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux"
::Restart
powershell -Command "Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile ~/Workspace/wsl/Ubuntu.zip -UseBasicParsing"
powershell -Command "Expand-Archive ~/Workspace/wsl/Ubuntu.zip ~/Workspace/wsl/Ubuntu"
~/Workspace/wsl/Ubuntu/ubuntu1804.exe