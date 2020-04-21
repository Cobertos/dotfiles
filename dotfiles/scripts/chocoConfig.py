import subprocess

#Export all the packages from choco list to packages.config

with open(f".\\packages.config", mode="w") as fp:
  #TODO: Make this interoperable with the environment options
  fp.write(f'<?xml version="1.0" encoding="utf-8"?>\n<packages>\n')
  chocoList = subprocess.run(['choco', 'list', '-lo', '-r', '-y'], capture_output=True)
  chocoList = chocoList.stdout.decode('utf-8')
  for line in chocoList.splitlines():
    [pkgId, pkgVersion] = line.split("|")
    fp.write(f'  <package id="{pkgId}"/>\n')
  fp.write(f'</packages>')