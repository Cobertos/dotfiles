#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.." || exit 1 # cd to dotfiles directory
# Setup ASDF vars
export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$HOME/bin:$PATH"

# https://github.com/asdf-community/asdf-python
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
asdf plugin add python https://github.com/asdf-community/asdf-python.git
# TODO: ??? did this package get removed? python-openssl 
sudo -E apt-get update && sudo -E apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
asdf install python 3.14.3
asdf set -u python 3.14.3
pip install requests