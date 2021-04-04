'''
Hotplug all my thunderbolt devices

Adapted from:
https://jpamills.wordpress.com/2017/03/18/hotplug-support-for-egpu-on-linux/
https://github.com/julianpoy/eGPUScripts/blob/master/switchGraphics-lightdm.sh
https://github.com/hertg/egpu-switcher/blob/master/egpu-switcher
'''

import os
import re
import sys
import subprocess
import time
from functools import partial
scriptDir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, scriptDir)
from df.SymLinkOp import SymLinkOp

print = partial(print, flush=True)

nvidiaPCIAddress = '/sys/bus/pci/devices/0000:3a:00.0'

thunderboltPCIAddresses = [
  # Graphics card
  nvidiaPCIAddress,
  # Thunderbolt 3 Belkin Hub on bottom port
  #'/sys/bus/pci/devices/0000:04:00.0'
]

def nvidiaDevices():
  '''
  Returns number of nvidia devices in use
  '''
  lsmodResult = subprocess.run(["lsmod"], check=True, capture_output=True)

  numDevices = 0
  for l in lsmodResult.stdout.decode('utf-8').split('\n'):
    # Format: 'Module                  Size  Used by'
    # Exampl: 'thunderbolt           167936  0'
    if l.startswith('nvidia_uvm') or l.startswith('nvidia_drm'):
      split = re.split(r'\s+', l)
      numDevices += int(split[2])
  return numDevices

def nvidiaGraphicsAttached():
  return os.path.exists(nvidiaPCIAddress)

LOG_RED = lambda s: f"\033[38;5;1m{s}\033[0m"
LOG_GREEN = lambda s: f"\033[38;5;2m{s}\033[0m"
LOG_YELLOW = lambda s: f"\033[38;5;3m{s}\033[0m"

if __name__ == "__main__":
  # Choose device, nvidia or intel. Default to NVIDIA if device is attached, though
  # this can be overriden by passing sys.argv[1] as "nvidia" or "intel"
  nvidiaOrIntel = "nvidia" if nvidiaGraphicsAttached() else "intel"
  if len(sys.argv) >= 2: # Override with sys.argv
    nvidiaOrIntel = "nvidia" if sys.argv[1] == "nvidia" else "intel"
  print(f"Setting system to {LOG_YELLOW(nvidiaOrIntel)} configuration")

  isDirty = False

  # TODO: Don't run this from not a tty, otherwise when the display-manager gets
  # killed, we won't have symlinked the xorg config yet (this is also included
  # in the TODO below)

  # 1, set prime-select to the proper thing
  # If you don't do this before setting the nvidia configuration, you will get an
  # error something like 'cannot find module name='off''
  # I didn't come across any issues when this is not set before using intel though
  # TODO: What exactly is this doing?
  primeQueryResult = subprocess.run(["prime-select", "query"], check=True, capture_output=True)
  primeNvidiaOrIntel = primeQueryResult.stdout.decode('utf-8').strip()
  if nvidiaOrIntel != primeNvidiaOrIntel:
    isDirty = True
    print(f"prime-select query returned '{primeNvidiaOrIntel}', setting to {nvidiaOrIntel}")
    subprocess.run(["prime-select", nvidiaOrIntel], check=True)

  # 2, teardown or setup NVIDIA kernel module
  # TODO: It would be best if the symlink for xorg always pointed at intel until we
  # knew for sure that nvidia was properly setup. Or if nvidia is being torn down,
  # it should set just before the teardown so that we have something to fallback on
  # if it fails?
  if nvidiaOrIntel == 'intel' and nvidiaGraphicsAttached():
    isDirty = True
    print("Tearing down NVIDIA device...")
    print(f"{LOG_YELLOW(str(nvidiaDevices()) + ' devices')} are using the nvidia kernel module")

    # Stop services relying on nvidia
    print("Stopping display-manager...")
    subprocess.run(["systemctl", "stop", "nvidia-persistenced.service"], check=True) #TODO: egpu switched never restarts this? do we need to do this?
    subprocess.run(["systemctl", "stop", "display-manager"], check=True)

    if nvidiaDevices() > 0:
      print(f"{LOG_RED(str(nvidiaDevices()) + ' devices')} are _still_ using the nvidia kernel module")
      print(f"{LOG_RED('Aborting... ')} try lsof /dev/nvidia* to figure out which ones")
      sys.exit(1)
    else:
      print(f"{LOG_GREEN(str(nvidiaDevices()) + ' devices')} are using the nvidia kernel module")

    # Remove the kernel module
    for d in ["nvidia_uvm", "nvidia_drm", "nvidia_modeset", "nvidia"]:
      subprocess.run(["modprobe", "-r", d], check=True)

    # Detach the PCI devices
    print(f"Detaching '{nvidiaPCIAddress}'...")
    subprocess.run(f"echo 1 | sudo tee {nvidiaPCIAddress}/remove", shell=True, check=True)
  elif nvidiaOrIntel == 'nvidia':
    # TODO: isDirty only true if nvidia is not already in use...
    isDirty = True
    # Do a pci rescan for previously removed devices
    subprocess.run(f"echo 1 | sudo tee /sys/bus/pci/rescan", shell=True, check=True)

    # Switching to nvidia, add the kernel module
    subprocess.run(["modprobe", "nvidia_drm"], check=True)

  # 3, symlink the xorg config properly
  xorgConf = f"xorg{'.egpu' if nvidiaOrIntel == 'nvidia' else ''}.conf"
  symLinkOp = SymLinkOp(f"{scriptDir}/X11/{xorgConf}", f"/etc/X11/xorg.conf")
  if symLinkOp.needsExecute():
    isDirty = True
    print("Symlinking xorg config...")
    symLinkOp()

  # 4, restart display-manager
  if isDirty:
    subprocess.run(["systemctl", "restart", "display-manager"], check=True)
