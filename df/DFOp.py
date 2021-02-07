import logging
import traceback

class DFOp:
  """
  Base class for dotfile operations. Call it like a function to execute as
  necessary (only if the test passes)
  """
  verifyOnly = False

  def __init__(self):
    self.logger = logging.getLogger(f"DFOp.{self.__class__.__name__}")

  def __call__(self):
    """Calls execute"""
    self.execute()

  def description(self):
    """Returns an optional description of this Op, shown next to the name"""
    return ''

  def needsExecute(self):
    """
    Returns if the operation needs an execute
    Should throw if the environment is not setup properly and other stuff needs
    to happen first.
    Can also return None, meaning always execute, even if verifyOnly is set
    """
    raise NotImplementedError

  def forceExecute(self):
    """
    Does the actual operation, regardless of what needsExecute() is
    """
    raise NotImplementedError

  def execute(self):
    """
    Runs the op if the needsExecute() passes. If DFOp.verifyOnly, it will only test
    needsExecute() and return, unless it returns None, then it forceExecute()s it
    """
    opName = self.__class__.__name__
    opDesc = self.description()
    def extra(action, ne=None):
      d = {
        'opAction': action,
        'opName': opName,
        'opDesc': opDesc,
      }
      if ne != None:
        d['opNeedsExecute'] = ne
      return d

    self.logger.debug("Enter op", extra=extra('start'))
    try:
      needsExecute = self.needsExecute()
    except Exception as e:
      self.logger.debug("Op fail", extra=extra('fail'))
      self.logger.exception(e)
      self.logger.debug("Leave op", extra=extra('end'))
      return

    # Don't show None tests
    if needsExecute != None:
      self.logger.debug("Op needs execute", extra=extra('ne', needsExecute))

    if needsExecute == False or (DFOp.verifyOnly and needsExecute != None):
      self.logger.debug("Leave op", extra=extra('end'))
      return #Only verifying (and test is not None) or it doesn't need execute

    try:
      self.forceExecute()
    except Exception as e:
      self.logger.debug("Op fail", extra=extra('fail'))
      self.logger.exception(e)
      self.logger.debug("Leave op", extra=extra('end'))
      return

    if needsExecute != None:
      self.logger.debug("Succeed op", extra=extra('succeed'))
    self.logger.debug("Leave op", extra=extra('end'))

class DFOpGroup(DFOp):
  """
  Base class for a group of DFOps
  """
  def __init__(self):
    super().__init__()
    self._ops = []

  def addOp(self, op):
    self._ops.append(op)

  def removeOp(self, op):
    self._ops.remove(op)

  def description(self):
    return self.groupName or f'{self.__class__.__name__} Group'

  def needsExecute(self):
    """Tests all the children"""
    return any([op.needsExecute() for op in self._ops])

  def forceExecute(self):
    """The actual op will execute all the children, if needsExecute passes for those children too"""
    for op in self._ops:
      op.execute()

# TODO
# class DFOpLogicalGroup(DFOpGroup):
#   """
#   Class for a group of DFOps with a shared name, added using the with statement.
#   Children will always be executed
#   """
#   # groupStack = []
#   currGroup = None

#   def __init__(self, groupName=None):
#     """
#     groupName is the name to show for the group in logging
#     """
#     super().__init__()
#     self.groupName = groupName

#   def __enter__(self):
#     # TODO: Might be too simple, but should work for our use case
#     # DFOpLogicalGroup.groupStack.append(self)
#     DFOpLogicalGroup.currGroup = self # DFOpLogicalGroup.groupStack[-1]
#     return self

#   def __exit__(self, exc_type, exc_value, tb):
#     # DFOpLogicalGroup.groupStack.pop()
#     # if len(DFOpGroup.groupStack):
#     #   DFOpLogicalGroup.currGroup = DFOpLogicalGroup.groupStack[-1]
#     if exc_type is not None:
#       traceback.print_exception(exc_type, exc_value, tb)
#       return False
#     return True

#   def description(self):
#     return self.groupName or f'{self.__class__.__name__} Group'

#   def needsExecute(self):
#     return None # No execute test, always forceExecute

LOG_RED = lambda s: f"\033[38;5;1m{s}\033[0m"
LOG_GREEN = lambda s: f"\033[38;5;2m{s}\033[0m"
LOG_YELLOW = lambda s: f"\033[38;5;3m{s}\033[0m"
LOG_LEFT = "\033[D"

class DFOpLoggingFormatter(logging.Formatter):
  """
  Formats the logging messages of the above two classes
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._opStack = []

  def format(self, record):
    # logDict = {
    #   'opName': opName,
    #   'opDesc': opDesc
    # }
    # action
    # test

    if not hasattr(record, 'opName'):
      # Newline because we turned off the terminator, and use the super class
      # to format it like normal
      return f'\n{super().format(record)}'

    if record.opAction == 'start':
      self._opStack.append(record.opName)
    elif record.opAction == 'end':
      self._opStack.pop()

    if record.opAction == 'end':
      return '\n'

    tag = {
      'start': '    ',
      'ne': LOG_YELLOW('TODO') if hasattr(record, 'opNeedsExecute') and record.opNeedsExecute else LOG_GREEN('NOOP'),
      'fail': LOG_RED('FAIL'),
      'succeed': LOG_GREEN(' OK ')
    }[record.opAction]

    nesting = (len(self._opStack) - 1) * '* '
    return f"\r{nesting}[{tag}] {record.opName} {record.opDesc}"