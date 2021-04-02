import sys
import subprocess
from .DFOp import DFOp, DFOpGroup

class PipInstallGlobalOp(DFOp):
  '''
  Runs a pip install --user, checks to make sure not in a venv
  '''
  def __init__(self, packageName):
    super().__init__()
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via pip?"

  def needsExecute(self):
    # Check if running in a virtualenv (want to install these globally
    # https://stackoverflow.com/a/1883251/2759427
    if hasattr(sys, 'real_prefix'):
      raise RuntimeError("Don't use in a virtualenv")

    testPackageName = self.packageName
    if "[" in self.packageName:
      # Uses setuptools/pip extras_require
      # TODO: This just rewrites it so that it will use the base name, but doesn't
      # actually ensure all the dependencies are installed
      testPackageName = self.packageName[0:self.packageName.find("[")]

    # https://askubuntu.com/questions/588390/
    # Also use sys.executable to use the current running python, regardless of what it is, assume pip is tied to it
    check = subprocess.run([sys.executable, "-c", f"import {testPackageName}"], stdout=subprocess.DEVNULL)
    return check.returncode != 0

  def forceExecute(self, *args):
    # Use the --user directory, makes it so we don't need root
    # TODO: Fix pipExecutable
    subprocess.run([pipExecutable, 'install', '--user', self.packageName, *args], check=True)

    # If asdf is installed, perform a reshim
    asdfInstalled = subprocess.run("type asdf", stdout=subprocess.DEVNULL, shell=True)
    asdfInstalled = asdfInstalled.returncode == 0
    if asdfInstalled:
      subprocess.run("asdf reshim", shell=True)

class PipXInstallGlobalOp(DFOpGroup):
  def __init__(self, packageName):
    super().__init__()
    self.packageName = packageName
    self.addOp(PipInstallGlobalOp("pipx"))

  def description(self):
    return f"'{self.packageName}' installed via pipx?"

  def needsExecute(self):
    needsPipX = super().needsExecute()
    if needsPipX:
      return True

    check = subprocess.run(f"pipx list | grep {self.packageName}", stdout=subprocess.DEVNULL, shell=True)
    return check.returncode != 0

  def forceExecute(self):
    super().forceExecute() # Install pipX if needed (.execute()s children)
    subprocess.run(["pipx", "ensurepath"], check=True)

    subprocess.run(["pipx", "install", self.packageName], check=True)
