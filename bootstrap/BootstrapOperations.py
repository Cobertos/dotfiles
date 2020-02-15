import traceback
import sys
import os
import shutil
import platform
import subprocess
from pathlib import Path, PurePosixPath
from utils import osEnvironNoExpand, getEnvironmentFilePath, event

class BootstrapOpRunner:
  def handleOp(self, op, *args, **kwargs):
    """
    Override in sub class to run ops in a with: statement
    """

  def __enter__(self):
    BootstrapOperation.opCall += self.handleOp

  def __exit__(self, exc_type, exc_value, tb):
    BootstrapOperation.opCall -= self.handleOp
    if exc_type is not None:
        traceback.print_exception(exc_type, exc_value, tb)
        return False
    return True


class BootstrapOperation:
  """
  Base class for bootstrap operations. Call it like a function, it's a callable
  """
  @event(static=True)
  def opCall(self):
    pass

  def __init__(self, *args, **kwargs):
    self.verify_only = False
    if 'verify_only' in kwargs:
      self.verify_only = bool(kwargs['verify_only'])
    self.environment = None
    if 'environment' in kwargs:
      self.environment = str(kwargs['environment'])
    self._called = False

  def __call__(self, *args, **kwargs):
    """
    Performs the operation
    """
    self._called = True
    BootstrapOperation.opCall(self, *args, **kwargs)

    # try:
    #   test = self.test()
    #   print(f"[{LOG_GREEN('OK')}] {self.description()}")
    # except Exception as e:
    #   test = False
    #   print(f"[{LOG_RED('NO')}] {self.description()}")
    #   print(e)
    # if self.verify_only or not test:
    #   return

    # self.execute(*args, **kwargs)

  def __del__(self):
    if not self._called:
      print(LOG_RED("Missed one"))

  #Has 3 functions that need to be implemented...
  #description
  #Returns a string with debugging output, should return fast
  #test
  #Returns if the operation needs to be performed or not
  #Should throw if the environment is not setup properly and other stuff needs
  #to happen first.
  #should return as fast as possible as the user might have to wait for this multiple
  #times an hour
  #execute
  #Does the actual operation, should only be called if test is false

# class AppendToFile(BootstrapOperation):
#   """
#   Appends string appendString to the file at path path
#   """
#   def __init__(self, appendString, path):
#     self.appendString = appendString
#     self.path = path

#   def description(self):
#     return f"'{self.path}' contains appendString?"

#   def test(self):
#     with open(self.path, mode="r") as fp:
#     #Go through the entire files, but reversed to succeed fast
#     for line in reversed(fp.readlines()):
#       if self.appendString.strip() in line.strip():
#         return True
#     return False

#   def execute(self):
#     with open(self.path, mode="a") as fp:
#       fp.write(self.appendString)

class SetEnvVar(BootstrapOperation):
  """
  Sets an EnvVar to a specific value
  """
  def __init__(self, value, envVar, **kwargs):
    super().__init__(**kwargs)
    self._value = value
    self.envVar = envVar

  @property
  def envValue(self):
    return self._value

  def description(self):
    return f"{self.envVar} is set to '{self.envValue}'?"

  def test(self):
    if self.envVar not in os.environ:
      return False
    return osEnvironNoExpand(self.envVar) == self.envValue

  def execute(self):
    
    #os.environ["PATH"] = f"{os.environ['PATH']};{path}"
    #TODO: os.environ doesn't persist on Windows, so instead use SETX
    #TODO: This will truncate the environment variable to 1024 characters too :/
    if platform.system() == "Windows":
      subprocess.run(["setx", "/m", self.envVar, f"{self.envValue}"])
    else:
      raise NotImplementedError("setEnvVar does not work on Linux variants :(")

class AppendToEnvVar(SetEnvVar):
  """
  Append the given path to the env var
  """
  def __init__(self, appendPath, envVar, prepend=False, **kwargs):
    super(SetEnvVar, self).__init__(**kwargs)
    self.appendPath = appendPath
    self.envVar = envVar
    self.prepend = prepend

  @property
  def envValue(self):
    return f"{self.appendPath};{osEnvironNoExpand(self.envVar)}" if self.prepend else \
      f"{osEnvironNoExpand(self.envVar)};{self.appendPath}"

  def description(self):
    return f"'{self.appendPath}' on {self.envVar}?"

  def test(self):
    if self.envVar not in os.environ:
      return False
    return self.appendPath in map(lambda p: p.strip(), osEnvironNoExpand(self.envVar).split(';'))

class AddToPath(AppendToEnvVar):
  """
  Adds a symlink at the given path pointing to target
  """
  #Requires admin on windows (the symlink permission)
  def __init__(self, path, prepend=False, **kwargs):
    super().__init__(path, "PATH", prepend, **kwargs)

class AddSymLink(BootstrapOperation):
  def __init__(self, target, path, **kwargs):
    super().__init__(**kwargs)
    #Determine which target to use based on environment
    self.target = getEnvironmentFilePath(target, self.environment)
    self.path = path

  def description(self):
    #[isLink, isLinkedProperly, linkResolved] = isProperlyLinked(path)
    #errStr = ('properly linked.' if isLinkedProperly else f"pointing to '{linkResolved}'.") if isLink else 'not a link.'
    #print(f"[{'OK' if isLinkedProperly else 'NO' }]: '{path}' is {errStr}")
    return f"'{self.path}' is properly linked to '{self.target}'?"

  def test(self):
    if not os.path.exists(self.target):
      #If target doesn't exist, Windows silently fails, so assert
      raise RuntimeError(f"Target '{self.target}' does not exist to be symlinked to.")

    isLink = os.path.islink(self.path)
    if not isLink:
      return False
    
    linkResolved = Path(self.path).resolve()
    isLinkedProperly = os.path.normpath(str(linkResolved)) == os.path.normpath(self.target)
    return isLinkedProperly

  def execute(self):
    parentPath = os.path.join(*os.path.split(self.path)[:-1])
    #TODO: Write this better...
    EnsureDirectory(parentPath, verify_only=self.verify_only, environment=self.environment)()
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

class EnsureDirectory(BootstrapOperation):
  def __init__(self, path, **kwargs):
    super().__init__(**kwargs)
    self.path = path

  def description(self):
    return f"'{self.path}' exists?"

  def test(self):
    return os.path.exists(self.path)

  def execute(self):
    os.makedirs(self.path)

npmRoot = None
class NpmInstallGlobal(BootstrapOperation):
  @staticmethod
  def npmRoot():
    global npmRoot
    if not npmRoot:
      npmRoot = subprocess.check_output("npm root -g", shell=True).decode("utf-8").strip()
    return npmRoot

  def __init__(self, packageName, **kwargs):
    super().__init__(**kwargs)
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via npm?"

  def test(self):
    #TODO: Does this work in all cases?
    return os.path.exists(os.path.join(NpmInstallGlobal.npmRoot(), *self.packageName.split('/')))

  def execute(self):
    subprocess.run(['npm', 'i', '-g', self.packageName], shell=True)


class PipInstallGlobal(BootstrapOperation):
  def __init__(self, packageName, **kwargs):
    super().__init__(**kwargs)
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via pip?"

  def test(self):
    # Check if running in a virtualenv (want to install these globally
    # https://stackoverflow.com/a/1883251/2759427
    if hasattr(sys, 'real_prefix'):
      raise RuntimeError("Don't use in a virtualenv")
    # https://askubuntu.com/questions/588390/
    check = subprocess.run(["python", "-c", f"\"import {self.packageName}\""], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return check.returncode == 0

  def execute(self, *args):
    subprocess.run(['pip', 'install', self.packageName, *args], shell=True)