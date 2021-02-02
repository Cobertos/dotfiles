import traceback
import subprocess
from functools import partial
from .BootstrapOp import BootstrapOp

#Overwrite print to always flush
print = partial(print, flush=True)
printnln = partial(print, end='')

class BootstrapOpRunner:
  """
  Collects created ops
  """
  def __init__(self):
    self.opExecStack = [] # Bookkeeping for current stack of operations

  def _handleOp(self, op, *args, **kwargs):
    """
    Handles some bookkeeping related to the operation while forwarding it off to
    the inheriting class
    """
    self.opExecStack.append(op)
    self.handleOp(op, *args, **kwargs)
    self.opExecStack.pop()

  def handleOp(self, op, *args, **kwargs):
    """
    Override in sub class to run ops in a with: statement
    """
    raise NotImplementedError

  def __enter__(self):
    BootstrapOp.opCall += self.handleOp

  def __exit__(self, exc_type, exc_value, tb):
    BootstrapOp.opCall -= self.handleOp
    if exc_type is not None:
        traceback.print_exception(exc_type, exc_value, tb)
        return False
    return True


LOG_RED = lambda s: f"\033[38;5;1m{s}\033[0m"
LOG_GREEN = lambda s: f"\033[38;5;2m{s}\033[0m"
LOG_YELLOW = lambda s: f"\033[38;5;3m{s}\033[0m"
LOG_LEFT = "\033[D"

class BootstrapLoggingOpRunner(BootstrapOpRunner):
  def __init__(self, verifyOnly):
    """
    Runner that logs out some pretty graphics and colors
    verifyOnly, only print that it will happen, but dont do it
    """
    super().__init__()
    self.verifyOnly = verifyOnly

  def handleOp(self, op, *args, **kwargs):
    opNestedLevel = len(self.opExecStack) - 1
    desc = op.description()
    if opNestedLevel >= 1:
      printnln("\n") # Print a new line to not overwrite our parent
    printnln(f"{'* '*opNestedLevel}[    ] {desc}")

    try:
      test = op.test()
      if test: #Did the test pass, is the Op already implemented?
        print(f"\r[{LOG_GREEN('NOOP')}] {desc}")
        return # Already done
      else:
        printnln(f"\r[{LOG_YELLOW('TODO')}] {desc}")
        if self.verifyOnly: #Only verifying, don't continue to execute
          print()
          return
    except Exception as e:
      print(f"\r[{LOG_RED('FAIL')}] {desc}")
      print(e)
      return

    try:
      op.execute(*args, **kwargs)
    except Exception as e:
      print(f"\r[{LOG_RED('FAIL')}] {desc}")
      # Fail catastrophically in case another operation down the line
      # relies on the one that just failed
      raise e

    print(f"\r[{LOG_GREEN(' OK ')}] {desc}")