#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.." || exit 1 # cd to dotfiles directory
# Setup ASDF vars
export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$HOME/bin:$PATH"

# https://github.com/asdf-vm/asdf-nodejs
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git
asdf install nodejs 24.14.1
asdf set -u nodejs 24.14.1
