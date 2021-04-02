import os
import subprocess
import requests
from .DFOp import DFOp

class AptKeyOp(DFOp):
  '''
  Adds a signing key with apt-key
  '''
  def __init__(self, keyLocation):
    super().__init__()
    self.keyLocation = keyLocation
    self._keyText = None

  def _getKeyText(self):
    if self._keyText:
      return
    if '://' in self.keyLocation:
      # Its a url
      self._keyText = requests.get(self.keyLocation).content
    else:
      raise NotImplementedError

  def description(self):
    return f"'{self.keyLocation}' key installed?"

  def needsExecute(self):
    self._getKeyText()
    # TODO: Need to test against apt-key list
    return True
    # https://stackoverflow.com/questions/1298066
    # check = subprocess.run(["dpkg", "-s", self.packageName], stdout=subprocess.DEVNULL)
    # return check.returncode == 0

    # return os.path.exists(os.path.join(NpmInstallGlobalOp.npmRoot(), *self.packageName.split('/')))

  def forceExecute(self):
    self._getKeyText()
    subprocess.run(['/usr/bin/pkexec', 'apt-key', 'add', '-'], input=self._keyText.decode("utf-8"), encoding="utf-8", check=True)