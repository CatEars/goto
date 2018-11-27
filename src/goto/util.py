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


def _do_echo(text, style, kwargs):
    '''Echoes with a prefered overridable style.'''
    values = dict(style)
    values.update(kwargs)
    click.secho(text, **values)


def pretty(text, **kwargs):
    '''Pretty print text (normal style print).'''
    _do_echo(text, config.STYLE, kwargs)


def detail(text, **kwargs):
    '''Eye catching printing.'''
    _do_echo(text, config.DETAIL, kwargs)


def boring(text, **kwargs):
    '''Boring/Structural printing.'''
    _do_echo(text, config.BORING, kwargs)


def error(text, **kwargs):
    '''Error printing.'''
    _do_echo(text, config.ERROR, kwargs)


def text_response(text):
    '''Fully "unstyled" text printing for bash/zsh communication.'''
    click.echo(text)
