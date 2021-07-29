import os
import shutil
from pathlib import Path
from .DFOp import DFOpGroup
from .EnsureDirectoryOp import EnsureDirectoryOp

class WriteFileOp(DFOpGroup):
  '''
  Creates a symlink at path, pointing to target
  Will prompt if something already exists at the target
  '''
  def __init__(self, path, content):
    super().__init__()
    #Determine which target to use based on environment
    self.path = path
    self.parentPath = os.path.join(*os.path.split(self.path)[:-1])
    self.content = content
    self.addOp(EnsureDirectoryOp(self.parentPath))

  def description(self):
    #[isLink, isLinkedProperly, linkResolved] = isProperlyLinked(path)
    #errStr = ('properly linked.' if isLinkedProperly else f"pointing to '{linkResolved}'.") if isLink else 'not a link.'
    #print(f"[{'OK' if isLinkedProperly else 'NO' }]: '{path}' is {errStr}")
    return f"'{self.path}' is written with custom content?"

  def needsExecute(self):
    return not os.path.isfile(self.path) or not open(self.path, 'r', encoding='utf-8').read() == self.content

  def forceExecute(self):
    super().forceExecute() # Call all the childrens .execute()s

    # Try delete file if it exists
    while os.path.isfile(self.path):
      if input("File to write already exists, delete? y/N ") == 'y':
        if os.path.isfile(self.path):
          os.remove(self.path)
        elif os.path.isdir(self.path):
          shutil.rmtree(self.path)
        else:
          raise RuntimeError("Path was not a file or directory") from e
      else:
        return

    # Write the file
    with open(self.path, 'w', encoding='utf-8') as f:
      f.write(self.content)
