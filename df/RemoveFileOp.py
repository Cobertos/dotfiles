from .DFOp import DFOp
import os

class RemoveFileOp(DFOp):
  def __init__(self, path):
    super().__init__()
    self.path = path

  def description(self):
    return f"'{self.path}' removed?"

  def needsExecute(self):
    return os.path.exists(self.path) and os.path.isfile(self.path)

  def forceExecute(self):
  	# TODO: What if the removal requires superuser?
    os.remove(self.path)