import sys
import traceback
from typing import NoReturn

from traceback_with_variables.core import Format, iter_tb_lines
from traceback_with_variables.print import print_tb as print_tb_


def overwrite(fmt: Format = Format()) -> NoReturn:
    def print_tb(tb, limit=None, file=sys.stderr):  # noqa
        print_tb_(e=ValueError(''), tb=tb, fmt=fmt, file_=file)

    def print_exception(etype, value, tb, limit=None, file=sys.stderr, chain=True):  # noqa
        print_tb_(e=value, tb=tb, file_=file, fmt=fmt)

    def print_exc(limit=None, file=sys.stderr, chain=True):  # noqa
        return print_exception(None, sys.exc_info()[1], sys.exc_info()[2], limit, file, chain)

    def print_last(limit=None, file=None, chain=True):  # noqa
        return print_exception(None, sys.last_value, sys.last_traceback, limit, file, chain)

    def format_exception(etype, value, tb, limit=None, chain=True):  # noqa
        return [line + '\n' for line in iter_tb_lines(e=value, tb=tb, fmt=fmt)]

    def format_exc(limit=None, chain=True):  # noqa
        return format_exception(None, sys.exc_info()[1], sys.exc_info()[2], limit, chain)

    traceback.print_tb = print_tb
    traceback.print_exception = print_exception
    traceback.print_exc = print_exc
    traceback.print_last = print_last
    traceback.format_exception = format_exception
    traceback.format_exc = format_exc
