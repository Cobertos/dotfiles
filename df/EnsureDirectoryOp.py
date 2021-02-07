from .DFOp import DFOp
import os

class EnsureDirectoryOp(DFOp):
  def __init__(self, path):
    super().__init__()
    self.path = path

  def description(self):
    return f"'{self.path}' exists?"

  def needsExecute(self):
    return not os.path.exists(self.path)

  def forceExecute(self):
    os.makedirs(self.path)