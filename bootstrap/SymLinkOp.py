import os
import shutil
from pathlib import Path
from .BootstrapOp import BootstrapOp
from .EnsureDirectoryOp import EnsureDirectoryOp

class SymLinkOp(BootstrapOp):
  def __init__(self, target, path):
    super().__init__()
    #Determine which target to use based on environment
    self.target = target
    self.path = path

  def description(self):
    #[isLink, isLinkedProperly, linkResolved] = isProperlyLinked(path)
    #errStr = ('properly linked.' if isLinkedProperly else f"pointing to '{linkResolved}'.") if isLink else 'not a link.'
    #print(f"[{'OK' if isLinkedProperly else 'NO' }]: '{path}' is {errStr}")
    return f"'{self.path}' is properly linked to '{self.target}'?"

  def test(self):
    isLink = os.path.islink(self.path)
    if not isLink:
      #logger.log(f"Path was not a link")
      return False
    
    linkResolved = Path(self.path).resolve()
    isLinkedProperly = os.path.normpath(str(linkResolved)) == os.path.normpath(self.target)
    #if not isLinkedProperly:
      #logger.log(f"Path was not a linked to correct location, instead {linkResolved}")
    return isLinkedProperly

  def execute(self):
    if not os.path.exists(self.target):
      #If target doesn't exist, Windows silently fails, so assert
      raise RuntimeError(f"Target '{self.target}' does not exist to be symlinked to.")

    parentPath = os.path.join(*os.path.split(self.path)[:-1])
    EnsureDirectoryOp(parentPath)()
    #Make the link and do things if it fails
    while not self.test():
      try:
        os.symlink(self.target, self.path)
      except FileExistsError as e:
        print(e)
        if input(f"File to symlink already exists, delete? y/N ") == 'y':
          if os.path.isfile(self.path):
            os.remove(self.path)
          elif os.path.isdir(self.path):
            shutil.rmtree(self.path)
          else:
            raise RuntimeError("Path was not a file or directory")
        else:
          return