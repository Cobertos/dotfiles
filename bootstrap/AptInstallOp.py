import os
import subprocess
from .BootstrapOp import BootstrapOp
from .AptKeyOp import AptKeyOp
from .AptRepositoryOp import AptRepositoryOp

npmRoot = None
class AptInstallOp(BootstrapOp):
  def __init__(self, packageName, addKey=None, addRepo=None):
    super().__init__()
    self.packageName = packageName
    self.aptKeyAdd = addKey
    self.aptRepoAdd = addRepo

  def description(self):
    return f"'{self.packageName}' installed via apt?"

  def test(self):
    # https://stackoverflow.com/questions/1298066
    check = subprocess.run(["dpkg", "-s", self.packageName], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return check.returncode == 0

    return os.path.exists(os.path.join(NpmInstallGlobalOp.npmRoot(), *self.packageName.split('/')))

  def execute(self):
    aptNeedsUpdate = False
    if self.aptKeyAdd:
      AptKeyOp(self.aptKeyAdd)()
      aptNeedsUpdate = True
    if self.aptRepoAdd:
      AptRepositoryOp(self.aptRepoAdd)()
      aptNeedsUpdate = True

    if aptNeedsUpdate:
      subprocess.run(['apt', 'update'], check=True)

    subprocess.run(['apt', 'install', self.packageName], check=True)