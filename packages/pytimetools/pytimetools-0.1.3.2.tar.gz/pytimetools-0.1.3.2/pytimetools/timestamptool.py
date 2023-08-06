#!/usr/bin/env python
"""
doc:
时间戳相关:
"""
import datetime
import time

from pytimetools.tztools import get_current_timezone


def get_timestamp():
    """

    :return:
    """
    return int(round(time.time()))


def get_timestamp_before_days(timestamp=None, days=0):
    """

    :param timestamp: 10位时间戳. 当前时间.
    :param days:
    :return:
    """
    if not timestamp:
        timestamp = get_timestamp()
    one_days = 60*60*24
    before_timestamp = timestamp - days*one_days
    return before_timestamp, timestamp


def get_timestamp_and_start_timestamp(timestamp=None):
    """
    项目上线时间.
    :param timestamp: 10位时间戳. 当前时间.
    :return:
    """
    if not timestamp:
        timestamp = get_timestamp()
    # utc+8: 2020-11-19 0:0:1
    # debug: 2020-11-18. 1605628801
    # before_timestamp = 1605628801
    before_timestamp = 1605715201
    return before_timestamp, timestamp


def get_timestamp_ms():
    """

    :return:
    """
    return int(round(time.time() * 1000))


def get_timestamp_and_ms():
    """

    :return:
    """
    timestamp = round(time.time())
    return int(timestamp), int(timestamp * 1000)


def timestamp_to_local(timestamp):
    """
    时间戳->local time 默认时区
    13位只取前10位

    :param timestamp: 10
    :return:
    """
    tz = get_current_timezone()
    local_time = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    return local_time


def is_timestamp_ms(timestamp):
    """

    :param timestamp:
    :return:
    """
    timestamp = int(timestamp)
    timestamp_length = len(str(timestamp))
    if timestamp_length != 13:
        raise TypeError('timestamp:({}) is not int or len({}) < 13'.format(
            type(timestamp), timestamp_length))
    return True
