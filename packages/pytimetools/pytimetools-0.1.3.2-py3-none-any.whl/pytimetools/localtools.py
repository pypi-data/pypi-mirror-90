#!/usr/bin/env python
"""
doc:
local time tools
"""
import datetime


def get_now():
    """

    :return:
    """
    return datetime.datetime.now()


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


def _get_passed_one_day_from_now(days=1):
    """
    获取过去距离今天的某一天
    :param days:
    :return:
    """
    today = get_now().today()
    passed_days = datetime.timedelta(days=days)
    passed_days_time = today - passed_days
    return passed_days_time


def get_yesterday():
    """
    :return:
    """
    return _get_passed_one_day_from_now(days=1).date()


def is_date_expired_local(now_date_local=None, other_date=None):
    """

    :param now_date_local:
    :param other_date:
    :return:
    """
    if not now_date_local:
        now_date_local = get_now().date()
    if not isinstance(other_date, datetime.date):
        raise TypeError('other_date:({}) is not datetime.date'.format(
            type(other_date)))
    return now_date_local > other_date
