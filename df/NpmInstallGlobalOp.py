import os
import subprocess
from .DFOp import DFOp

npmRoot = None
class NpmInstallGlobalOp(DFOp):
  '''
  Runs an npm install -g, runs asdf reshim after as well
  '''
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

  def needsExecute(self):
    # Checks whether the current npm root has the given package folder
    # Also works for packages like @vue/cli
    return not os.path.exists(os.path.join(NpmInstallGlobalOp.npmRoot(), *self.packageName.split('/')))

  def forceExecute(self):
    # NOTE: We use this to skip reshimming behavior in asdf, which is a real pain
    # this also requires shell=True, env={ ... } wasn't working :c
    # https://github.com/asdf-vm/asdf-nodejs/issues/46
    subprocess.run(f'ASDF_SKIP_RESHIM=1 npm install -g {self.packageName}', shell=True, check=True)

    # If asdf is installed, perform a reshim
    asdfInstalled = subprocess.run("type asdf", stdout=subprocess.DEVNULL, shell=True)
    asdfInstalled = asdfInstalled.returncode == 0
    if asdfInstalled:
      subprocess.run("asdf reshim", shell=True, check=True)
