
from contextlib import contextmanager
from simplejson import load, dump

from .context import context as _context

__all__ = 'context',

@contextmanager
def json(filename, iterable_as_array=True, indent=False, **kwargs):
    """mutable json context
    """
    global load, dump
    try:
        with open(filename) as stream:
            obj = load(stream, **kwargs)
    except FileNotFoundError:
        obj = {}
    try:
        yield obj
    finally:
        with open(filename, 'w') as stream:
            dump(obj, stream, iterable_as_array=iterable_as_array, indent=indent, **kwargs)


@contextmanager
def context(*args, **kwargs):
    global _context, json
    with _context() as ctx:
        with json(*args, **kwargs) as data:
            ctx.update(data)
            try:
                yield ctx
            finally:
                data.update(ctx)
