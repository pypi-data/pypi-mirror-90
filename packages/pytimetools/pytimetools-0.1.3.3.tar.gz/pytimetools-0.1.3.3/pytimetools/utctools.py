#!/usr/bin/env python
"""
doc:
utc time tools
utc:
utc -> local
utc -> timestamp
utc -> gmt
"""
import datetime

import pytz

from pytimetools.tztools import get_current_timezone


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


def utc_to_localtime(utctime):
    """
    naive time 与 active time的概念
    1.数据库中的DateTimeFiled需要转换localtime
    2.前端传入的时间最好时utctime

    astimezone:
        可以将一个时区的时间转换成另一个时区的时间,
        前提是这个被转换的时间必须是一个aware时间
    https://www.cnblogs.com/limaomao/p/9257014.html
    :param utctime:
    :return:
    """
    # naive time(不知道自己时区) => aware time(有时区)
    utc = utctime.replace(tzinfo=pytz.UTC)
    local_time = utc.astimezone(get_current_timezone())
    return local_time


def utc_to_gmt(utc_time):
    """
    UTC -> GMT
    :param utc_time:
    :return:
    """
    # todo
    pass


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
    timestamp = utc_to_timestamp(utc_time)
    return int(timestamp) * 1000

