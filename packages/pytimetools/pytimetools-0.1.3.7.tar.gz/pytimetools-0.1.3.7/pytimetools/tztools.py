#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
目前设定时区是上海. utc+8
"""
import pytz

DEFAULT_TZ_UTC = "UTC"
DEFAULT_TZ_SH = "Asia/Shanghai"


def get_current_timezone():
    """
    todo: 可以动态配置
    :return:
    """
    # from django.utils import timezone
    # return timezone.get_current_timezone()
    return pytz.timezone(DEFAULT_TZ_SH)


def get_utc_timezone():
    return pytz.UTC


def get_timezone(time_zone=''):
    """
    TIME_ZONE = 'Asia/Shanghai'
    TIME_ZONE = 'UTC'
    Return the default time zone as a tzinfo instance.

    This is the time zone defined by settings.TIME_ZONE.
    """
    return pytz.timezone(time_zone)
