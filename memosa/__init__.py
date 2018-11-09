#!/usr/bin/env python3.7

import logging
from functools import partial, wraps
from collections import defaultdict
from contextlib import contextmanager
from contextvars import ContextVar
from inspect import isgeneratorfunction

from simplejson import load, dump

__all__ = 'context', 'json', 'memoize1'

_context = ContextVar('memosa.context')

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

@decorator
def memoize1(func, label=None):
    "use qualname and first argument to memoize"
    "memoization requires context"

    partition_key = label or func.__qualname__

    if isgeneratorfunction(func):
        get_value = lambda key : tuple(func(key))
    else:
        get_value = func

    @wraps(func)
    def memoized(key):
        nonlocal func, partition_key, get_value
        try:
            context = _context.get()
        except LookupError:
            # no context, memoization is disabled
            return get_value(key)
        else:
            memoized = context[partition_key]
            try:
                obj = memoized[key]
            except KeyError:
                logger.info('cache miss %s %s' % (partition_key, key))
                obj = memoized[key] = get_value(key)
            else:
                logger.info('cache hit %s %s' % (partition_key, key))
            return obj

    return memoized

@decorator
def wraps_context(func, if_exists=False):
    "if running in memoization context, apply wrapper"
    @contextmanager
    def custom_context(*args, **kwargs):
        try:
            current_context = _context.get()
        except LookupError:
            if if_exists:
                yield
            else:
                with context() as current_context:
                    with func(current_context, *args, **kwargs) as value:
                        yield current_context if value == None else value
        else:
            with func(current_context, *args, **kwargs) as value:
                yield current_context if value == None else value
    return custom_context

@wraps_context
@contextmanager
def json(context, filename, use_decimal=False, iterable_as_array=True):
    """
    persist context in JSON format
    note that keys will be converted to strings!
    """
    global load, dump
    load = partial(load, use_decimal=use_decimal)
    dump = partial(dump, use_decimal=use_decimal, iterable_as_array=iterable_as_array)
    try:
        logger.info('loading %r (json) into %r' % (filename, context))
        with open(filename) as stream:
            context.update(load(stream))
        logger.info('loaded %r (json) into %r' % (filename, context))
    except FileNotFoundError:
        logger.info('json not found %r' % filename)
    finally:
        try:
            yield
        finally:
            logger.info('saving %r to %r (json)' % (context, filename))
            with open(filename, 'w') as stream:
                dump(context, stream)

@contextmanager
def context():
    "initializes memoization context"
    obj = Context()
    token = _context.set(obj)
    try:
        logger.info('entering context %r' % obj)
        yield obj
    finally:
        logger.info('leaving context %r' % obj)
        _context.reset(token)

class Context(defaultdict):
    """
    {qualname: {memoize key : memoized value}}
    """

    def __init__(self):
        super().__init__(dict)

    def __repr__(self):
        if len(self) < 100:
            summary = ','.join('%s[%s]' % (key, len(value)) for key, value in self.items())
        else:
            summary = ','.join(self)
        return '<memosa.Context[%s]>' % summary

    def run(self, func, *args, **kwargs):
        "run a function in this context -- useful for threading"
        token = _context.set(self)
        try:
            return func(*args, **kwargs)
        finally:
            _context.reset(token)
