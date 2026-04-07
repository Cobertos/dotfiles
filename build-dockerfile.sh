#!/bin/bash

set -euo pipefail

#!/bin/bash
set -euo pipefail

# Get the current git hash
GIT_HASH=$(git rev-parse --short HEAD)
DOTFILES_VERSION="0.0.1"

# Check if the git work tree is dirty (uncommitted changes)
if [ -n "$(git status --porcelain)" ]; then
    # Dirty work tree: append '-ephemeral' to the git hash, do NOT tag with DOTFILES_VERSION
    GIT_TAG="${GIT_HASH}-ephemeral"
    echo "Dirty work tree detected. Tagging with git hash only: ${GIT_TAG}"
    docker build --progress=plain \
        -t "dev-container-yippee:${GIT_TAG}" \
        -f dev.Dockerfile .
else
    # Clean work tree: tag with both DOTFILES_VERSION and the git hash
    GIT_TAG="${GIT_HASH}"
    echo "Clean work tree. Tagging with DOTFILES_VERSION and git hash: ${GIT_TAG}"
    docker build --progress=plain \
        -t "dev-container-yippee:${DOTFILES_VERSION}" \
        -t "dev-container-yippee:${GIT_TAG}" \
        -f dev.Dockerfile .
fi