import sys
import subprocess
from .BootstrapOp import BootstrapOp

class PipInstallGlobalOp(BootstrapOp):
  def __init__(self, packageName):
    super().__init__()
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via pip?"

  def test(self):
    # Check if running in a virtualenv (want to install these globally
    # https://stackoverflow.com/a/1883251/2759427
    if hasattr(sys, 'real_prefix'):
      raise RuntimeError("Don't use in a virtualenv")
    # https://askubuntu.com/questions/588390/
    check = subprocess.run(["python3", "-c", f"import {self.packageName}"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    #print(check)
    #print(subprocess.check_output(f"python3 -c \"import {self.packageName}\"", shell=True).decode("utf-8").strip())
    return check.returncode == 0

  def execute(self, *args):
    subprocess.run(['pip', 'install', self.packageName, *args], check=True)