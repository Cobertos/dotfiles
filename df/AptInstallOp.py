import os
import subprocess
import tempfile
import requests
from .DFOp import DFOpGroup
from .AptKeyOp import AptKeyOp
from .AptRepositoryOp import AptRepositoryOp

npmRoot = None
class AptInstallOp(DFOpGroup):
  def __init__(self, packageName, addKey=None, addRepo=None, debUrl=None):
    super().__init__()
    self.packageName = packageName
    self.debUrl = debUrl
    if addKey:
      self.addOp(AptKeyOp(addKey))
    if addRepo:
      self.addOp(AptRepositoryOp(addRepo))

  def description(self):
    return f"'{self.packageName}' installed via apt?"

  def needsExecute(self):
    # https://stackoverflow.com/questions/1298066
    check = subprocess.run(["dpkg", "-s", self.packageName], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return check.returncode != 0

  def forceExecute(self):
    aptNeedsUpdate = super().needsExecute() # Check all the children
    super().forceExecute() # Run all the children executes

    if aptNeedsUpdate:
      subprocess.run(['apt', 'update'], check=True)

    if self.debUrl:
      # Download the debUrl to a temporary file in a temporary directory
      # TODO: Might want to fix
      # 'N: Download is performed unsandboxed as root as file '/tmp/tmpy8ri9opf/discord.tmp.deb'
      # couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)'
      # which happens
      with tempfile.TemporaryDirectory() as tmpDirName:
        tmpFileName = os.path.join(tmpDirName, f'{self.packageName}.tmp.deb')
        with requests.get(self.debUrl, stream=True) as r:
          r.raise_for_status()
          with open(tmpFileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
              f.write(chunk)

        # Install the tmp deb file
        subprocess.run(['apt', 'install', tmpFileName], check=True)
    else:
      subprocess.run(['apt', 'install', self.packageName], check=True)