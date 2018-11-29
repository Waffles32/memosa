
from functools import wraps, partial
from inspect import isgeneratorfunction
import logging, warnings

from .context import current_context, context
from .json import context as _json_context

__all__ = 'context', 'memoize1', 'memoize2', 'json'

logger = logging.getLogger(__name__)

def decorator(func):
    "allows decorator to take kwargs like @your_decorator(x=1)"
    "also helps document your function as a decorator"
    @wraps(func)
    def decorate(*args, **kwargs):
        if args:
            return func(*args, **kwargs)
        else:
            return partial(func, **kwargs)
    return decorate


def _memoize(alias, key, func):
    """
    """
    global current_context
    try:
        context = current_context.get()
    except LookupError:
        value = func()
    else:
        cache = context[alias]
        key = str(key) # fix for JSON
        try:
            value = cache[key]
        except KeyError:
            logger.info('cache miss %s %s' % (alias, key))
            value = cache[key] = func()
        else:
            logger.info('cache hit %s %s' % (alias, key))
    return value

@decorator
def memoize1(func, label=None):
    """
    decorated function must accept one argument
    str(argument) will be used to cache the returned value
    if the function is a generator the result will be a tuple
    """
    alias = label or func.__qualname__

    if isgeneratorfunction(func):
        func2 = lambda key : tuple(func(key))
    else:
        func2 = func

    @wraps(func)
    def wrap(key):
        global _memoize
        nonlocal func2, alias
        return _memoize(alias, key, lambda : func2(key))
    return wrap

@decorator
def memoize2(func, label=None):
    """
    decorated function is a generator
    first yield is the cache key (usually created from the arguments)
    second yield is the value, which will only execute on cache miss

    @memoize2
    def add(x, y):
        yield f'{x}+{y}'
        yield x + y
    """
    alias = label or func.__qualname__
    @wraps(func)
    def wrap(*args, **kwargs):
        global _memoize
        nonlocal func, alias
        gen = func(*args, **kwargs)
        return _memoize(alias, next(gen), lambda : next(gen))
    return wrap


def json(*args, **kwargs):
    warnings.warn("memosa.json() will be removed.  use memosa.json.context() instead", category=DeprecationWarning, stacklevel=2)
    return _json_context(*args, **kwargs)
