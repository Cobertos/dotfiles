FROM ubuntu:22.04

ENV TZ=America/New_York

ARG DEBIAN_FRONTEND=noninteractive
RUN yes | /usr/local/sbin/unminimize
RUN apt-get update -y && \
  apt-get install -y curl bash git ca-certificates xz-utils sudo systemd

# Setup user
RUN groupadd -g 1000 cobertos && \
    useradd -m -u 1000 -g 1000 -s /bin/bash cobertos && \
    echo "cobertos ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER cobertos

# Copy and run bootstrapping, use environment "container" to only install those things
COPY --chown=1000:1000 bootstrap/ /dotfiles/bootstrap/
WORKDIR /dotfiles
RUN /dotfiles/bootstrap/0-bootstrap-asdf.sh
RUN /dotfiles/bootstrap/1-bootstrap-asdf-python.sh
RUN /dotfiles/bootstrap/2-bootstrap-asdf-nodejs.sh
ENV PATH="/home/cobertos/.asdf/shims:/home/cobertos/bin:${PATH}"

# Required for bootstrap AptInstallOp
RUN sudo apt-get update -y && \
  sudo apt-get install -y software-properties-common
# Copy everything else in the dotfiles repo into the container
# (this includes asdf)
COPY --chown=1000:1000 . /dotfiles
RUN test ! -f /dotfiles/secrets.sh || (echo "Failsafe: secrets.sh should not have been copied into the build!" && exit 1)
# Run final bootstrapping stage
ENV DOTFILES_ENVIRONMENT=container
RUN /home/cobertos/.asdf/installs/python/3.14.3/bin/python /dotfiles/bootstrap.py --yes

CMD ["sleep", "infinity"]
# STOPSIGNAL SIGRTMIN+3
# CMD ["/sbin/init"]
# CMD ["/bin/systemd"]

# ===========================================================
# TODO: At some point I would like to switch this to nix?
# # Nix paths
# # ENV PATH=/nix/var/nix/profiles/default/bin:$PATH
# # ENV NIX_PATH=/nix/var/nix/profiles/per-user/root/channels

# # Copy flake and activate it
# WORKDIR /opt/flake
# COPY dev.nix .

# # Pre-fetch flake inputs
# RUN nix --extra-experimental-features "nix-command flakes" \
#   flake update

# # Install tools from flake
# RUN nix profile install --extra-experimental-features "nix-command flakes" \
#     .#default
# {
#   description = "Tools for Ubuntu container";

#   inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";

#   outputs = { self, nixpkgs, ... }:
#     let pkgs = import nixpkgs { system = "x86_64-linux"; };
#     in {
#       packages.x86_64-linux.default = pkgs.buildEnv {
#         name = "tools";
#         paths = [
#           pkgs.sublime3
#           pkgs.fd
#           pkgs.nmap
#           pkgs.xclip
#         ];
#       };
#     };
# }