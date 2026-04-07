import os
import subprocess
import tempfile
import requests
from .DFOp import DFOp, DFOpGroup
from .AptKeyOp import AptKeyOp
from .AptRepositoryOp import AptRepositoryOp

class AptInstallOp(DFOpGroup):
  '''
  Runs an apt install of a package
  Can optionally add a key and package repository too
  '''
  def __init__(self, packageName, addKey=None, addRepo=None):
    super().__init__()
    self.packageName = packageName
    if addKey:
      self.addOp(AptKeyOp(addKey))
    if addRepo:
      self.addOp(AptRepositoryOp(addRepo))

  def description(self):
    return f"'{self.packageName}' installed via apt?"

  def needsExecute(self):
    # https://stackoverflow.com/questions/1298066
    check = subprocess.run(["dpkg", "-s", self.packageName], stdout=subprocess.DEVNULL)
    return check.returncode != 0

  def forceExecute(self):
    aptNeedsUpdate = super().needsExecute() # Check all the children
    super().forceExecute() # Run all the children executes

    yArg = ['-y'] if DFOp.autoAccept else []
    cmd = 'sudo' if os.environ.get('DOTFILES_ENVIRONMENT') == 'container' else '/usr/bin/pkexec'

    if aptNeedsUpdate:
      subprocess.run([cmd, 'apt-get', 'update'] + yArg, check=True)

    print("WILL DO", ['apt-get', 'install'] + yArg + [self.packageName])
    subprocess.run([cmd, 'apt-get', 'install'] + yArg + [self.packageName], check=True)
