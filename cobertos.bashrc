
# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

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

# asdf, for python and node version control
# https://asdf-vm.com
source "${cobconf}/deps/asdf/asdf.sh"
source "${cobconf}/deps/completions/asdf.bash"

# Z, a fuzzy 'cd' sort of program
# https://github.com/rupa/z
source "${cobconf}/deps/z/z.sh"

# Other stuff, default with Linux Mint, slightly modified
source ${cobconf}/default.sh

# Tools
findcode() {
  # Finds string in code files path or contents
  # Old Iterations
  #grep --exclude-dir={node_modules,.git,dist,FORKED,venv,Library,_nuxt} --exclude={*.min.js,*.js.map,*-lock.json,*.fbx} -RnI ~/Seafile/projects -e "$1"
  # TODO: Maybe use .gitignore with git check-ignore?
  # https://unix.stackexchange.com/questions/358270/find-files-that-are-not-in-gitignore
  # Prune sections will prune those subtrees from search but always evaluate to false
  find ~/Seafile/projects \
    -type d \( \
      -name node_modules -o -name .git -o -name .pytest_cache -o -name dist -o \
      -name __pycache__ -o -name FORKED -o -name venv -o -name Library -o -name _nuxt -o \
      -name reveal.js-dependencies -o -name .nuxt -o -path dotfiles/deps \
    \) -prune -false -o \
    -type f -a -not \( \
      -name '*.min.js' -o -name '*.js.map' -o -name '*-lock.json' -o -name '*.fbx' -o \
      -name '*.dll' -o -name '*.exe' -o -name '*.mp4' -o -name '*.png' -o -name '*.jpg' -o \
      -name '*.jpeg' -o -name '*.kra' -o -name '*.pdn' -o -name '*.zip' -o -name '*.7z' -o \
      -name '*.meta' -o -name '*.gif' -o -name '*.tif' -o -name '*.ogg' \
    \) | xargs -d '\n' egrep -n "$1"
    #-type f -exec egrep -l "$1" '{}' + -print
    #-type f -path "*$1*" -o \
}
findnotes() {
  grep --include=*.md -RnI ~/Seafile/notes -e "$1"
}

# Verify the setup
if ! cobverify; then
  while true; do
    read -p "Verification has failed, do you wish to perform an install? (y/n)" yn
    case $yn in
      [Yy]* ) cobsetup; break;;
      * ) echo "Ignoring verification failure and dropping into shell"; break;;
    esac
  done
fi

}

init
unset init

