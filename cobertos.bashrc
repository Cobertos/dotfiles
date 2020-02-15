init () {

#General
wrk="$HOME/Workspace"
export wrk

cobconf="${BASH_SOURCE%/*}"
export cobconf

alias cobconf="subl ${cobconf}"
cobverify () {
    python "${cobconf}/bootstrap/cli.py" --verify-only
}
cobsetup () {
    python "${cobconf}/bootstrap/cli.py"
}
alias gitcc="git --git-dir=${cobconf}/.git --work-tree=${cobconf}"

#Git aliases
alias gitkcon='git log --all --decorate --oneline --graph'

#ConEmu Integration
if [[ -n "${ConEmuPID}" ]]; then
  #For WSL and cygwin/msys connector (which ConEmu will use for Git bash). It
  #sends an operating system command (OSC) to cygwin/msys connector to update the
  #cwd on PS1 print (the \$PWD in the below string, \w will not work).
  #https://conemu.github.io/en/ShellWorkDir.html#connector-ps1
  #https://github.com/Maximus5/ConEmu/issues/1752
  PS1="\[\e]9;9;\"\$PWD\"\007\e]9;12\007\]$PS1"
fi

#z
source "${cobconf}/scripts/z.sh"

#Verify the setup
if ! cobverify; then
    while true; do
        read -p "Verification has failed, do you wish to perform an install? (y/n)" yn
        case $yn in
            [Yy]* ) cobsetup; break;;
            [Nn]* ) break;;
            * ) echo "Please answer y or n.";;
        esac
    done
fi
}

init
unset init