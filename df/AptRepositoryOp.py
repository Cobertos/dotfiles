import os
import subprocess
import requests
from .DFOp import DFOp

class AptRepositoryOp(DFOp):
  '''
  Adds an apt repository
  '''
  def __init__(self, repository):
    super().__init__()
    self.repository = repository

  def description(self):
    return f"'{self.repository}' repository sourcing?"

  def needsExecute(self):
    return True # TODO

  def forceExecute(self):
    cmd = 'sudo' if os.environ.get('DOTFILES_ENVIRONMENT') == 'container' else '/usr/bin/pkexec'
    subprocess.run([cmd, 'add-apt-repository', self.repository], check=True)