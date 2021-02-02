import os
import subprocess
import requests
from .BootstrapOp import BootstrapOp

npmRoot = None
class AptKeyOp(BootstrapOp):
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

  def test(self):
    self._getKeyText()
    # TODO: Need to test against apt-key list
    return False
    # https://stackoverflow.com/questions/1298066
    # check = subprocess.run(["dpkg", "-s", self.packageName], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # return check.returncode == 0

    # return os.path.exists(os.path.join(NpmInstallGlobalOp.npmRoot(), *self.packageName.split('/')))

  def execute(self):
    self._getKeyText()
    subprocess.run(['/usr/bin/pkexec', 'apt-key', 'add', '-'], input=self._keyText.decode("utf-8"), encoding="utf-8", check=True)