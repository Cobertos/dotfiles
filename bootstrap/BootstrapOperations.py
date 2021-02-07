import traceback
import sys
import os
import shutil
import platform
import subprocess
import winreg
import logging
import filecmp
from pathlib import Path, PurePosixPath
from utils import osEnvironNoExpand, event, vTypeToStr, registryToStr

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

  def __init__(self):
    self.logger = logging.getLogger(f"BootstrapOperation.{self.__class__.__name__}")
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
  def __init__(self, value, envVar):
    super().__init__()
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
  def __init__(self, appendPath, envVar, prepend=False):
    super(SetEnvVar, self).__init__()
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
  def __init__(self, path, prepend=False):
    super().__init__(path, "PATH", prepend)

class AddSymLink(BootstrapOperation):
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
    if not os.path.exists(self.target):
      #If target doesn't exist, Windows silently fails, so assert
      raise RuntimeError(f"Target '{self.target}' does not exist to be symlinked to.")

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
    parentPath = os.path.join(*os.path.split(self.path)[:-1])
    #TODO: Write this better...
    EnsureDirectory(parentPath)()
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
  def __init__(self, path):
    super().__init__()
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

  def __init__(self, packageName):
    super().__init__()
    self.packageName = packageName

  def description(self):
    return f"'{self.packageName}' installed via npm?"

  def test(self):
    #TODO: Does this work in all cases?
    return os.path.exists(os.path.join(NpmInstallGlobal.npmRoot(), *self.packageName.split('/')))

  def execute(self):
    subprocess.run(['npm', 'i', '-g', self.packageName], shell=True)


class PipInstallGlobal(BootstrapOperation):
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
    check = subprocess.run(["python", "-c", f"\"import {self.packageName}\""], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return check.returncode == 0

  def execute(self, *args):
    subprocess.run(['pip', 'install', self.packageName, *args], shell=True)

class SetRegKey(BootstrapOperation):
  """
  Sets a registry key, creates and sets if it doesn't exist
  Fails if the registry path to the key does not exist
  """
  def __init__(self, registry, subKey, key, vType, value):
    super().__init__()
    self.registry = registry
    self.subKey = subKey
    self.key = key
    self.vType = vType
    self.value = value

  @property
  def regPath(self):
    return f"{registryToStr(self.registry)}\\{self.subKey}\\{self.key}"

  def description(self):
    return f"'{self.regPath}' is set to '{self.value}' ({vTypeToStr(self.vType)})?"

  def test(self):
    try:
      with winreg.OpenKey(self.registry, self.subKey, 0, winreg.KEY_READ | winreg.KEY_WRITE) as regKey:
        checkValue, checkType = winreg.QueryValueEx(regKey, self.key)
    except WindowsError as e:
      if e.winerror != 2:
        raise e #Not a "File not found" exception
      self.logger.info(e)
      self.logger.info("Key didnt exist")
      return False #Key didn't exist, most likely

    self.logger.info(f"'{self.regPath}' is currently set to {checkValue} ({vTypeToStr(checkType)})")
    return checkType == self.vType and checkValue == self.value

  def execute(self):
    with winreg.CreateKeyEx(self.registry, self.subKey, 0, winreg.KEY_READ | winreg.KEY_WRITE) as regKey:
      winreg.SetValueEx(regKey, self.key, 0, self.vType, self.value)

class SetTheme(BootstrapOperation):
  """
  Check that the theme is set to the right file, windows 10 tested only
  """
  def __init__(self, themePath):
    super().__init__()
    self.themePath = themePath

  def description(self):
    return f"Is theme path set to '{self.themePath}'?"

  def test(self):
    #Windows 10 tested only...
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes') as regKey:
      value, vType = winreg.QueryValueEx(regKey, 'CurrentTheme')
      self.logger.info(f"Current theme is '{value}'.")
      if not os.path.exists(value): #Theme referenced doesnt exist
        return False
      return filecmp.cmp(value, self.themePath, shallow=False)

  def execute(self):
    #There's a couple ways to install the theme
    #https://stackoverflow.com/questions/546818/how-do-i-change-the-current-windows-theme-programmatically
    #Invoking the theme seems to be the most forward thinking solution
    #NOTE: This will make Windows actually copy the folder into the
    #themes folder... We can't actually symlink or Windows will actually try
    #to install the theme as a xxx (2).theme file. This is the best we can do
    subprocess.run([self.themePath], shell=True)