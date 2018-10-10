
#Git aliases
alias gitkcon='git log --all --decorate --oneline --graph'

#ConEmu Integration
if [[ -n "${ConEmuPID}" ]]; then
  #For WSL, Sends an operating system command (OSC) to cygwin/msys connector to
  #update the cwd on PS1 print (the \w).
  #https://conemu.github.io/en/ShellWorkDir.html#connector-ps1
  PS1="\[\e]9;9;\"\w\"\007\e]9;12\007\]$PS1"
fi
if [[ ( -n "${ConEmuPID}" ) && ( -x "$(command -v ConEmuC)" ) ]]; then
  #For non-wsl, calls ConEmuC if it exists and will store cwd
  #https://conemu.github.io/en/ShellWorkDir.html#bash_and_other_cygwin_shells
  PROMPT_COMMAND="ConEmuC -StoreCWD"
fi