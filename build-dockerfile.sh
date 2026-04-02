#!/bin/bash

set -euo pipefail

# Builds the docker file
# --progress=plain makes it not pretty but prints everything
docker build --progress=plain -t dev-container-yippee -f dev.Dockerfile .