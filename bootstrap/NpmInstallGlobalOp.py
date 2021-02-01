import os
import subprocess
from .BootstrapOp import BootstrapOp

npmRoot = None
class NpmInstallGlobalOp(BootstrapOp):
  @staticmethod
  def npmRoot():
    global npmRoot
    if not npmRoot:
      npmRoot = subprocess.check_output(['npm', 'root', '-g']).decode("utf-8").strip()
    return npmRoot

  def __init__(self, packageName):
    super().__init__()
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via npm?"

  def test(self):
    #TODO: Does this work in all cases?
    return os.path.exists(os.path.join(NpmInstallGlobalOp.npmRoot(), *self.packageName.split('/')))

  def execute(self):
    subprocess.run(['npm', 'install', '-g', self.packageName], check=True)