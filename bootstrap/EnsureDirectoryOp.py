from .BootstrapOp import BootstrapOp
import os

class EnsureDirectoryOp(BootstrapOp):
  def __init__(self, path):
    super().__init__()
    self.path = path

  def description(self):
    return f"'{self.path}' exists?"

  def test(self):
    return os.path.exists(self.path)

  def execute(self):
    os.makedirs(self.path)