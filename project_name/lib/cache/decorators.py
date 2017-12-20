import functools


class memoize(object):
    """
    Cache return value of an instance method
    This class is meant to be used as a decorator of methods. The return value
    from a given method invocation will be cached on the instance whose method
    was invoked. All arguments passed to a method decorated with memoize must
    be hashable.
    Author: http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return functools.partial(self, obj)

    def __call__(self, *args, **kwargs):
        obj = args[0]
        if not hasattr(obj, '_cache'):
            obj._cache = {}

        key = (self.func, args[1:], frozenset(kwargs.items()))
        if key not in obj._cache:
            obj._cache[key] = self.func(*args, **kwargs)

        return obj._cache[key]


class memoize_invalidate(object):
    """
    Use in conjunction with @memoize decorator when you want to reset instance cache
    when calling a specific method
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return functools.partial(self, obj)

    def __call__(self, *args, **kwargs):
        obj = args[0]
        obj._cache = {}
        return self.func(*args, **kwargs)
