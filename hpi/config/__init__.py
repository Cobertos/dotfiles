### HPI personal config
## see
# https://github.com/karlicoss/HPI/blob/master/doc/SETUP.org#setting-up-modules
# https://github.com/karlicoss/HPI/blob/master/doc/MODULES.org
## for some help on writing your own config

from my.core import Paths, PathIsh, get_files

class reddit:
  '''
  Uses [[https://github.com/karlicoss/rexport][rexport]] output.
  Requires you set it up with the Reddit integration and the point it at the 
  ~/Seafile/archive/Exported...
  python3 -m rexport.export --secrets ~/.hpi-reddit-secrets.py >"${HOME}/Seafile/archive/ExportedServiceData/reddit/export-$(date -I).json"
  '''
  export_path: Paths = '/home/cobertos/Seafile/archive/ExportedServiceData/reddit/'