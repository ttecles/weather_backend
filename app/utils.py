import datetime as dt
import traceback
from collections import Iterable

import six


def get_now():
    return dt.datetime.now()


def is_string_types(var):
    return isinstance(var, six.string_types)


def is_iterable(var):
    return isinstance(var, Iterable)


def is_iterable_not_string(var):
    return is_iterable(var) and not is_string_types(var)


def format_exception(exc: Exception) -> str:
    return ''.join(traceback.format_exception(exc, exc, exc.__traceback__))
