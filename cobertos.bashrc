init () {



# Meta (dotfiles related)
cobconf="${BASH_SOURCE%/*}"
export cobconf

alias cobconf="subl ${cobconf}"
cobverify () {
    python3 "${cobconf}/bootstrap.py" --verify-only
}
cobsetup () {
    python3 "${cobconf}/bootstrap.py"
}
alias gitcc="git --git-dir=${cobconf}/.git --work-tree=${cobconf}"

# Git aliases
alias gitkcon='git log --all --decorate --oneline --graph'

alias explr="nemo"
alias lclip="xclip -selection clipboard"

# ConEmu Integration
if [[ -n "${ConEmuPID}" ]]; then
  # For WSL and cygwin/msys connector (which ConEmu will use for Git bash). It
  # sends an operating system command (OSC) to cygwin/msys connector to update the
  # cwd on PS1 print (the \$PWD in the below string, \w will not work).
  # https://conemu.github.io/en/ShellWorkDir.html#connector-ps1
  # https://github.com/Maximus5/ConEmu/issues/1752
  PS1="\[\e]9;9;\"\$PWD\"\007\e]9;12\007\]$PS1"
fi

# z
source "${cobconf}/scripts/z.sh"

# Other stuff, default with Linux Mint, slightly modified
source ${cobconf}/default.sh

# Verify the setup
if ! cobverify; then
  while true; do
    read -p "Verification has failed, do you wish to perform an install? (y/n)" yn
    case $yn in
      [Yy]* ) cobsetup; break;;
      * ) echo "Ignoring verification failure and continueing"; break;;
    esac
  done
fi

}

init
unset init

