#!/usr/bin/env python
"""
doc:
"""
import functools

import pytz
from django.utils import timezone


def get_current_timezone():
    return timezone.get_current_timezone()


def get_utc_timezone():
    return pytz.UTC


@functools.lru_cache()
def get_timezone(time_zone=''):
    """
    TIME_ZONE = 'Asia/Shanghai'
    TIME_ZONE = 'UTC'
    Return the default time zone as a tzinfo instance.

    This is the time zone defined by settings.TIME_ZONE.
    """
    return pytz.timezone(time_zone)
