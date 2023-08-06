# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import logging
import typing
import functools

import click

def _get_command_qualname(ctx: click.Context):
    def iter_names(ctx: click.Context):
        if ctx.parent:
            yield from iter_names(ctx.parent)
        if ctx.info_name:
            yield ctx.info_name.replace('.', '_')
    return '.'.join(list(iter_names(ctx)))

def get_logger():
    'get logger for current command.'
    ctx = click.get_current_context()
    qualname = _get_command_qualname(ctx)
    logger = logging.getLogger(qualname)
    return logger

LOGGING_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'WARN': logging.WARN,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}

def attach_logger_options(command=None, default_logto='<stderr>'):
    '''
    attach some `log*` options on the command.

    return a decorator to decorate the command.
    '''

    def decorator(target):
        if target is None:
            raise TypeError

        @functools.wraps(target)
        def wrapper(*args, loglevel, logto, **kwargs):
            logger = get_logger()
            if loglevel is not None:
                logger.setLevel(LOGGING_LEVELS[loglevel])

            if logto:
                handler = None
                if logto == '<stdout>':
                    handler = logging.StreamHandler(sys.stdout)
                elif logto == '<stderr>':
                    handler = logging.StreamHandler(sys.stderr)
                else:
                    # test path
                    try:
                        with open(logto, 'a'):
                            pass
                    except:
                        pass
                    else:
                        handler = logging.FileHandler(logto, encoding='utf-8')

                logger.handlers.clear()
                if handler:
                    logger.handlers.append(handler)

            return target(*args, **kwargs)

        options = [
            click.option('--loglevel', 'loglevel', type=click.Choice(LOGGING_LEVELS, False), default='WARNING'),
            click.option('--logto', 'logto', default=default_logto),
        ]

        wrapper = wrapper
        for option in options:
            wrapper = option(wrapper)
        return wrapper

    return decorator(command) if command else decorator
