import sys
import subprocess
import sys
from .DFOp import DFOp, DFOpGroup

class PipInstallGlobalOp(DFOp):
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
    # https://askubuntu.com/questions/588390/
    # Also use sys.executable to use the current running python, regardless of what it is, assume pip is tied to it
    check = subprocess.run([sys.executable, "-c", f"import {self.packageName}"], stdout=subprocess.DEVNULL)
    #print(check)
    #print(subprocess.check_output(f"python3 -c \"import {self.packageName}\"", shell=True).decode("utf-8").strip())
    return check.returncode != 0

  def forceExecute(self, *args):
    subprocess.run([pipExecutable, 'install', self.packageName, *args], check=True)

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