import plistlib
import re
import sys
import os
from math import floor
from pathlib import PurePath
from datetime import datetime

def itermcolors_dict_color_to_conemu(color):
  """
  Convert a single itemcolor plist dict from the plist into a conemu, 0xBBGGRR color
  """
  def dectohex(dec):
    return str(hex(floor(float(dec)*255)))[2:]

  return "00" + \
    dectohex(color["Blue Component"]) + \
    dectohex(color["Green Component"]) + \
    dectohex(color["Red Component"])

def itermcolors_dict_to_conemu(pl, name="DefaultName"):
  """
  Converts a itermcolors dictionary (pulled from plist file)
  @param {dict} pl The dict containing all the itermcolors
  """
  #Convert every iterm color to a conemu color
  for k,v in pl.items():
    pl[k] = itermcolors_dict_color_to_conemu(v)
  #Map it to the conemu theme template
  return f'''
\t<key name="Palette1" modified="{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" build="190714">
\t\t<value name="Name" type="string" data="{name}"/>
\t\t<value name="TextColorIdx" type="hex" data="10"/>
\t\t<value name="BackColorIdx" type="hex" data="10"/>
\t\t<value name="PopTextColorIdx" type="hex" data="10"/>
\t\t<value name="PopBackColorIdx" type="hex" data="10"/>
\t\t<value name="ColorTable00" type="dword" data="{pl["Background Color"]}"/>  <!-- Black (Background) -->
\t\t<value name="ColorTable01" type="dword" data="{pl["Ansi 4 Color"]}"/>  <!-- DarkBlue (Module names in Jupyter) -->
\t\t<value name="ColorTable02" type="dword" data="{pl["Ansi 2 Color"]}"/>  <!-- DarkGreen (Diff add in Git, Commments in Posh, built-ins in Jupyter) -->
\t\t<value name="ColorTable03" type="dword" data="{pl["Ansi 6 Color"]}"/>  <!-- DarkCyan (String in Posh, Comments in Jupyter) -->
\t\t<value name="ColorTable04" type="dword" data="{pl["Ansi 1 Color"]}"/>  <!-- DarkRed (Diff remove in Git) -->
\t\t<value name="ColorTable05" type="dword" data="{pl["Ansi 5 Color"]}"/>  <!-- DarkMagenta (Setup questions in Sphinx) -->
\t\t<value name="ColorTable06" type="dword" data="{pl["Ansi 3 Color"]}"/>  <!-- DarkYellow -->
\t\t<value name="ColorTable07" type="dword" data="{pl["Ansi 7 Color"]}"/>  <!-- Gray (Default Text) -->
\t\t<value name="ColorTable08" type="dword" data="{pl["Ansi 8 Color"]}"/>  <!-- DarkGray (Parameters) -->
\t\t<value name="ColorTable09" type="dword" data="{pl["Ansi 12 Color"]}"/>  <!-- Blue -->
\t\t<value name="ColorTable10" type="dword" data="{pl["Ansi 10 Color"]}"/>  <!-- Green -->
\t\t<value name="ColorTable11" type="dword" data="{pl["Ansi 14 Color"]}"/>  <!-- Cyan -->
\t\t<value name="ColorTable12" type="dword" data="{pl["Ansi 9 Color"]}"/>  <!-- Red -->
\t\t<value name="ColorTable13" type="dword" data="{pl["Ansi 13 Color"]}"/>  <!-- Magenta -->
\t\t<value name="ColorTable14" type="dword" data="{pl["Ansi 11 Color"]}"/>  <!-- Yellow (Exception in IPython) -->
\t\t<value name="ColorTable15" type="dword" data="{pl["Ansi 15 Color"]}"/>  <!-- White (Number, Git diff text) -->
\t</key>'''

def itermcolors_to_conemu(path):
  '''
  Converts an .itermcolors file to an xml datastructure
  that can be used with ConEmu
  '''
  #Open itermcolors and parse with plistlib
  with open(path, 'rb') as fp:
    pl = plistlib.load(fp)
  #Convert to conemu theme
  conemuColors = itermcolors_dict_to_conemu(pl, PurePath(path).stem)
  return conemuColors

if __name__ == "__main__":
  if not len(sys.argv) > 1:
    raise TypeError("No .itermcolors was given. \n\nUSAGE: itermcolors2conemu [XXX.itermcolors]")
  #print to stdout
  print(itermcolors_to_conemu(sys.argv[1]))