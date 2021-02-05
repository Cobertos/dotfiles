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
    # NOTE: We use this to skip reshimming behavior in asdf, which is a real pain
    # this also requires shell=True, env={ ... } wasn't working :c
    # https://github.com/asdf-vm/asdf-nodejs/issues/46
    subprocess.run(f'ASDF_SKIP_RESHIM=1 npm install -g {self.packageName}', shell=True, check=True)

    # If asdf is installed, perform a reshim
    asdfInstalled = subprocess.run("type asdf", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
    asdfInstalled = asdfInstalled.returncode == 0
    if asdfInstalled:
      subprocess.run("asdf reshim", shell=True)