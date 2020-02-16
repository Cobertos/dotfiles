import winreg
import os
import json

def getDropboxDir():
  """
  Finds the dropbox folder programatically from a few different files
  https://help.dropbox.com/installs-integrations/desktop/locate-dropbox-folder#programmatically
  """
  appData = os.environ["APPDATA"]
  #Find the dropbox info json
  dropboxInfoFile = None
  if os.path.isfile(f"{appData}\\Dropbox\\info.json"):
      dropboxInfoFile = f"{appData}\\Dropbox\\info.json"
  elif os.path.isfile(f"{os.environ['LOCALAPPDATA']}\\Dropbox\\info.json"):
      dropboxInfoFile = f"{os.environ['LOCALAPPDATA']}\\Dropbox\\info.json"
  #Open the json and extract the key we need for the personal path
  with open(dropboxInfoFile) as fp:
      return json.load(fp)["personal"]["path"]

def osEnvironNoExpand(envVar):
  """
  You have to get the variable from the Windows registry to not expand
  """
  with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment") as regKey:
    return winreg.QueryValueEx(regKey, envVar)[0]
    #Close is autocalled on GC

def vTypeToStr(vType):
  return [t[1] for t in [(winreg.REG_BINARY, 'REG_BINARY'),
    (winreg.REG_DWORD, 'REG_DWORD'),
    (winreg.REG_DWORD_LITTLE_ENDIAN, 'REG_DWORD_LITTLE_ENDIAN'),
    (winreg.REG_DWORD_BIG_ENDIAN, 'REG_DWORD_BIG_ENDIAN'),
    (winreg.REG_EXPAND_SZ, 'REG_EXPAND_SZ'),
    (winreg.REG_LINK, 'REG_LINK'),
    (winreg.REG_MULTI_SZ, 'REG_MULTI_SZ'),
    (winreg.REG_NONE, 'REG_NONE'),
    (winreg.REG_QWORD, 'REG_QWORD'),
    (winreg.REG_QWORD_LITTLE_ENDIAN, 'REG_QWORD_LITTLE_ENDIAN'),
    (winreg.REG_RESOURCE_LIST, 'REG_RESOURCE_LIST'),
    (winreg.REG_FULL_RESOURCE_DESCRIPTOR, 'REG_FULL_RESOURCE_DESCRIPTOR'),
    (winreg.REG_RESOURCE_REQUIREMENTS_LIST, 'REG_RESOURCE_REQUIREMENTS_LIST'),
    (winreg.REG_SZ, 'REG_SZ')] if t[0] == vType][0]

def registryToStr(registry):
  return [r[1] for r in [(winreg.HKEY_CLASSES_ROOT, 'HKEY_CLASSES_ROOT'),
    (winreg.HKEY_CURRENT_USER, 'HKEY_CURRENT_USER'),
    (winreg.HKEY_LOCAL_MACHINE, 'HKEY_LOCAL_MACHINE'),
    (winreg.HKEY_USERS, 'HKEY_USERS'),
    (winreg.HKEY_PERFORMANCE_DATA, 'HKEY_PERFORMANCE_DATA'),
    (winreg.HKEY_CURRENT_CONFIG, 'HKEY_CURRENT_CONFIG'),
    (winreg.HKEY_DYN_DATA, 'HKEY_DYN_DATA')] if r[0] == registry][0]

def getEnvironmentFilePath(path, environment):
  return f"{path}##{environment}" if environment and os.path.exists(f"{path}##{environment}") else path

def event(stateful=None, static=False):
    """
    Decorator that can be called with or without args.

    Creates a boundevent accessed at the decorated function
    """
    func = None
    if callable(stateful):
        func = stateful
    else:
        stateful = bool(stateful)

    class _event(object):
        """
        Descriptor to handle instance and static access
        of a function that fronts a boundevent
        """
        def __init__(self, func):
            """
            func {Function} decorator
            """
            self.__doc__ = func.__doc__
            self._key = ' ' + func.__name__
        def __get__(self, obj, cls):
            target = cls if static else obj
            try:
                return getattr(target, self._key)
            except AttributeError:
                be = boundevent(stateful)
                setattr(target, self._key, be)
                return be

    #Return created _event if func because only a func was passed and we use default arguments
    #otherwise, send back _event because we got the arguments but still need to wrap a func
    return _event(func) if func else _event

class boundevent(object):
    '''
    An object that acts as a C#-like event, where handlers can be += and -=
    when called will call all the handlers with the given args.

    Use the @event decorator to decorate existing functions to get docstrings
    as well
    '''
    def __init__(self, stateful=False):
        """
        stateful {Boolean} Whether or not the handler has state. If True,
        newly added handlers will be called with the most recent call
        arguments (say, for an event that happens that future handlers need to know about)
        """
        self._fns = []
        self._stateful = stateful
        self._state = False
    def __iadd__(self, fn):
        #Stateful and previously called
        self._fns.append(fn)
        if self._state and self._stateful:
            fn(*self._state[0], **self._state[1])
        return self
    def __isub__(self, fn):
        self._fns.remove(fn)
        return self
    def __call__(self, *args, **kwargs):
        self._state = [args, kwargs]
        for f in self._fns[:]:
            f(*args, **kwargs)