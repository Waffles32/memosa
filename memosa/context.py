
from collections import defaultdict
from contextlib import contextmanager
from contextvars import ContextVar

current_context = ContextVar(__name__ + '.current_context')

@contextmanager
def context():
    """context to store memoization data
    """
    context = defaultdict(dict)
    token = current_context.set(context)
    try:
        yield context
    finally:
        current_context.reset(token)


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
