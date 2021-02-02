import os
import subprocess
import requests
from .BootstrapOp import BootstrapOp

npmRoot = None
class AptRepositoryOp(BootstrapOp):
  def __init__(self, repository):
    super().__init__()
    self.repository = repository

  def description(self):
    return f"'{self.repository}' repository sourcing?"

  def test(self):
    return False # TODO

  def execute(self):
    subprocess.run(['/usr/bin/pkexec', 'add-apt-repository', self.repository], check=True)
    subprocess.run(['apt', 'update'], check=True)