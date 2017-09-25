from functools import wraps

# https://stackoverflow.com/questions/6407993/how-to-memoize-kwargs
def memoize(fun):
    """A simple memoize decorator for functions supporting positional args."""
    @wraps(fun)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))
        try:
            ret = cache[key]
            print "Returning cache",fun, args, kwargs
            return ret
        except KeyError:
            print "Evaluate",fun, args, kwargs
            ret = cache[key] = fun(*args, **kwargs)
        return ret
    cache = {}
    return wrapper

@memoize
def f( x, y ):
    return x + y

def g( x, y ):
    return x - y
