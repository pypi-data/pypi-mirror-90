#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
time format tools
"""

DEFAULT_FMT = "%Y-%m-%d %H:%M:%S"
DEFAULT_FMT_GMT = "%a, %d %b %Y %H:%M:%S GMT"


def fmt_time(naive_time, fmt=DEFAULT_FMT):
    """
    datetime.datetime.strftime

    :param naive_time:
    :param fmt:
    :return:
    """
    return naive_time.strftime(fmt)


def fmt_utc_to_gmt(date_time_utc=None, fmt=DEFAULT_FMT_GMT):
    """

    :param date_time_utc:
    :param fmt:
    :return:
    """
    return date_time_utc.strftime(fmt)
