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

# class commits:
# '''
# local Filesystem git repo commits
# From https://github.com/karlicoss/HPI/blob/master/my/coding/commits.py (search 'config')
# '''
#   # TODO: Use the output of `find ~/Seafile/projects/*/*.git` (Basically, all non-forked or whatever else projects, also make sure to check repo and repository!)
#   roots: Paths = []
#   emails: List = ['me@cobertos.com', 'me+git@cobertos.com', 'minimalist37@gmail.com']
#   names: List = []

# class my.github.gdpr
# class my.github.ghexport