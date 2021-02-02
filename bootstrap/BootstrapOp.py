import logging
from .utils import event

LOG_RED = lambda s: f"\033[38;5;1m{s}\033[0m"

class BootstrapOp:
  """
  Base class for bootstrap operations. Call it like a function, it's a callable
  """
  @event(static=True)
  def opCall(self):
    pass

  def __init__(self):
    self.logger = logging.getLogger(f"BootstrapOp.{self.__class__.__name__}")
    self._called = False

  def __call__(self, *args, **kwargs):
    """
    Performs the operation
    """
    self._called = True
    # Ops simply notify a OpRunner listening to the static opCall event when they
    # are called. The runner will do all the executing and logging
    # It also allows for nested Ops to occur in execute and the runner will handle
    # those too!
    BootstrapOp.opCall(self, *args, **kwargs)

  def __del__(self):
    if not self._called:
      # Op was created but never called, which is most likely a bug
      print(LOG_RED(f"Missed instance of {type(self).__name__}. {self.description()}"))

  def description(self):
    """Returns a string with debugging output, should return fast"""
    raise NotImplementedError

  def test(self):
    """
    Returns if the operation needs to be performed or not
    Should throw if the environment is not setup properly and other stuff needs
    to happen first.
    """
    raise NotImplementedError

  def execute(self):
    """
    Does the actual operation, should only be called if test is false
    """
    raise NotImplementedError