'''Utility functions used inside goto.'''

import click
from . import config

def cond(*args):
    '''Advanced conditional branching.'''
    predicate_and_handlers = args

    def do_handler(handler_or_value, args, kwargs):
        '''Returns either $1(*args, **kwargs) or $1 if $1 is not a function.'''
        if not callable(handler_or_value):
            return handler_or_value
        return handler_or_value(*args, **kwargs)

    def inner(*args, **kwargs):
        '''Inner function that is equivalent to the cond statement.'''
        for predicate, handler_or_value in predicate_and_handlers:
            if callable(predicate) and predicate(*args, **kwargs):
                return do_handler(handler_or_value, args, kwargs)
            if not callable(predicate) and predicate:
                return do_handler(handler_or_value, args, kwargs)
        return None

    return inner


def pretty(text):
    click.secho(text, **config.STYLE)
