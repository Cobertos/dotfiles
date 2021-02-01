import os

def getEnvironmentFilePath(path, environment):
  return f"{path}##{environment}" if environment and os.path.exists(f"{path}##{environment}") else path

def event(stateful=None, static=False):
    """
    Decorator that can be called with or without args.

    Creates a boundevent accessed at the decorated function
    """
    func = None
    if callable(stateful):
        func = stateful
    else:
        stateful = bool(stateful)

    class _event(object):
        """
        Descriptor to handle instance and static access
        of a function that fronts a boundevent
        """
        def __init__(self, func):
            """
            func {Function} decorator
            """
            self.__doc__ = func.__doc__
            self._key = ' ' + func.__name__
        def __get__(self, obj, cls):
            target = cls if static else obj
            try:
                return getattr(target, self._key)
            except AttributeError:
                be = boundevent(stateful)
                setattr(target, self._key, be)
                return be

    #Return created _event if func because only a func was passed and we use default arguments
    #otherwise, send back _event because we got the arguments but still need to wrap a func
    return _event(func) if func else _event

class boundevent(object):
    '''
    An object that acts as a C#-like event, where handlers can be += and -=
    when called will call all the handlers with the given args.

    Use the @event decorator to decorate existing functions to get docstrings
    as well
    '''
    def __init__(self, stateful=False):
        """
        stateful {Boolean} Whether or not the handler has state. If True,
        newly added handlers will be called with the most recent call
        arguments (say, for an event that happens that future handlers need to know about)
        """
        self._fns = []
        self._stateful = stateful
        self._state = False
    def __iadd__(self, fn):
        #Stateful and previously called
        self._fns.append(fn)
        if self._state and self._stateful:
            fn(*self._state[0], **self._state[1])
        return self
    def __isub__(self, fn):
        self._fns.remove(fn)
        return self
    def __call__(self, *args, **kwargs):
        self._state = [args, kwargs]
        for f in self._fns[:]:
            f(*args, **kwargs)