import os
import subprocess
from .BootstrapOp import BootstrapOp

npmRoot = None
class AptInstallOp(BootstrapOp):
  def __init__(self, packageName):
    super().__init__()
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via apt?"

  def test(self):
    # https://stackoverflow.com/questions/1298066
    check = subprocess.run(["dpkg", "-s", self.packageName], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return check.returncode == 0

    return os.path.exists(os.path.join(NpmInstallGlobalOp.npmRoot(), *self.packageName.split('/')))

  def execute(self):
    subprocess.run(['apt', 'install', self.packageName], check=True)