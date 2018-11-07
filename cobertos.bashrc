
#Git aliases
alias gitkcon='git log --all --decorate --oneline --graph'

#ConEmu Integration
if [[ -n "${ConEmuPID}" ]]; then
  #For WSL and cygwin/msys connector (which ConEmu will use for Git bash). It
  #sends an operating system command (OSC) to cygwin/msys connector to update the
  #cwd on PS1 print (the \w in the below string).
  #https://conemu.github.io/en/ShellWorkDir.html#connector-ps1
  PS1="\[\e]9;9;\"\w\"\007\e]9;12\007\]$PS1"
fi
