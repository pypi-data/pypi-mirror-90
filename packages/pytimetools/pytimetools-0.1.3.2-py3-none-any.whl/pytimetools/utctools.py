#!/usr/bin/env python
"""
doc:
utc time tools
"""
import datetime

import pytz


def get_now(tz=pytz.UTC):
    """

    :return: 返回tz时区的当前时间, 默认返回utc时间
    """
    return datetime.datetime.now(tz=tz)


def get_now_from_delta(seconds=1):
    """
    获取过去距离今天现在的某一天
    :param seconds:
    :return:
    """
    now = get_now()
    seconds = datetime.timedelta(seconds=seconds)
    passed_time = now - seconds
    return passed_time


def utc_to_timestamp(utc_time):
    """
    时间戳转utc
    :param utc_time:
    :return:
    """
    timestamp = utc_time.timestamp()
    return timestamp


def utc_to_timestamp_ms(utc_time):
    """
    时间戳转utc
    :param utc_time:
    :return:
    """
    timestamp = utc_time.timestamp()
    return int(timestamp) * 1000
