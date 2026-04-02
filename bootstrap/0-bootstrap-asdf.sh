#!/bin/bash

set -euo pipefail

# Download asdf from releases page and untar into home directory
mkdir -p "$HOME/bin"
export PATH="$HOME/bin:$PATH"
curl -fsSL "https://github.com/asdf-vm/asdf/releases/download/v0.18.1/asdf-v0.18.1-linux-amd64.tar.gz" \
  | tar -xz -C "$HOME/bin"
