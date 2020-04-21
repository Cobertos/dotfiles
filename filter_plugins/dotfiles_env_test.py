import os

def dotfiles_env_test(path, env):
  envPath = path + '##' + env
  return envPath if os.path.exists(envPath) else path

class FilterModule(object):
  def filters(self):
    return {
      'dotfiles_env_test': dotfiles_env_test
    }