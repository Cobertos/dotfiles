import os
import subprocess
import platform

def getEnvironmentFilePath(path, environment):
  return f"{path}##{environment}" if environment and os.path.exists(f"{path}##{environment}") else path

def getUserHome():
  if platform.system() != "Windows":
    currUser = subprocess.check_output(['logname']).decode('utf-8').strip()
    return f"/home/{currUser}" # There are more general ways but this is good enough
  else:
    return os.environ["USERPROFILE"]
