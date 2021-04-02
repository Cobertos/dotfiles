import os
import subprocess
import platform

def getEnvironmentFilePath(path, environment):
  '''
  For a given path, appends the environemnt as a suffix if the environment path exists
  '''
  return f"{path}##{environment}" if environment and os.path.exists(f"{path}##{environment}") else path

def getUserHome():
  '''
  Gets the home folder of the user
  '''
  if platform.system() == "Windows":
    return os.environ["USERPROFILE"]

  # assume linux
  currUser = subprocess.check_output(['logname']).decode('utf-8').strip()
  return f"/home/{currUser}" # There are more general ways but this is good enough
