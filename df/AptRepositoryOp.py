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
    subprocess.run(['/usr/bin/pkexec', 'add-apt-repository', self.repository], check=True)