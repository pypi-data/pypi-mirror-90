#!/usr/bin/env python
"""
doc:
"""

import datetime
import time
import pytz
from django.utils import timezone
from django.utils.timezone import get_current_timezone


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


def get_now_local():
    """

    :return:
    """
    return datetime.datetime.now()


def _get_passed_one_day_from_now(days=1):
    """
    获取过去距离今天的某一天
    :param days:
    :return:
    """
    today = get_now_local().today()
    passed_days = datetime.timedelta(days=days)
    passed_days_time = today - passed_days
    return passed_days_time


def get_yesterday():
    """

    :return:
    """
    return _get_passed_one_day_from_now(days=1).date()


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
    local_time = utc.astimezone(timezone.get_current_timezone())
    return local_time


def localtime_to_timestamp(local_time):
    """

    :param local_time:
    :return:
    """
    return time.mktime(local_time.timetuple())


def localtime_to_timestamp_ms(local_time):
    """

    :param local_time:
    :return:
    """
    return int(localtime_to_timestamp(local_time))*1000


def localtime_to_utc(local_time):
    """
    localtime -> utc
    1.本地时区转为时间戳
    2.时间戳转为utc

    上海1927改表, 故不使用replace
    :param local_time:
    :return:
    """
    timestamp = localtime_to_timestamp(local_time)
    return timestamp_to_utc(timestamp)


def timestamp_to_utc(timestamp):
    """
    时间戳转utc
    :param timestamp:
    :return:
    """
    utc_time = datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)
    return utc_time


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


def fmt_time(naive_time):
    """
    datetime.datetime.strftime

    :param naive_time:
    :return:
    """
    fmt = '%Y-%m-%d %H:%M:%S'
    return naive_time.strftime(fmt)


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


def is_date_expired_local(now_date_local=None, other_date=None):
    """

    :param now_date_local:
    :param other_date:
    :return:
    """
    if not now_date_local:
        now_date_local = get_now_local().date()
    if not isinstance(other_date, datetime.date):
        raise TypeError('other_date:({}) is not datetime.date'.format(
            type(other_date)))
    return now_date_local > other_date


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


def is_timestamp_expired_local(timestamp=None, other_timestamp=None,
                               timeout=60*1*10*1000):
    """

    :param timestamp:
    :param other_timestamp:
    :param timeout:
    :return:
    """
    if not timestamp:
        timestamp = get_timestamp_ms()
    other_timestamp = int(other_timestamp)
    is_timestamp_ms(other_timestamp)
    # timestamp < (other_timestamp + timeout)
    ttl = other_timestamp + timeout - timestamp
    return ttl
