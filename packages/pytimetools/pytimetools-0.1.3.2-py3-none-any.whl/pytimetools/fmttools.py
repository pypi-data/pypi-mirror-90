#!/usr/bin/env python
"""
doc:
time format tools
"""


def fmt_time(naive_time):
    """
    datetime.datetime.strftime

    :param naive_time:
    :return:
    """
    fmt = '%Y-%m-%d %H:%M:%S'
    return naive_time.strftime(fmt)
