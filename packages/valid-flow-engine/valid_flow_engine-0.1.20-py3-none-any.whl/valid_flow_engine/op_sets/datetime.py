from typing import Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from valid_flow_engine.op_set_registry import register_op_set, as_op


@register_op_set
class DateTimeOpSet:
    @staticmethod
    @as_op(display='Is Before', help_text='If Date 1 is before Date 2')
    def is_before(date1: datetime, date2: datetime):
        return date1 < date2

    @staticmethod
    @as_op(display='Is After', help_text='If Date 1 is after Date 2')
    def is_after(date1: datetime, date2: datetime):
        return date1 > date2

    @staticmethod
    @as_op(display='Is Equal', help_text='If Date 1 is equal to Date 2')
    def is_same_date(date1: datetime, date2: datetime):
        return date1.date() == date2.date()

    @staticmethod
    @as_op(display='Chage Datetime', help_text='Calcualte time based on provided delta, use `-` to move into past')
    def change(
        date: datetime,
        years: Optional[int] = None,
        months: Optional[int] = None,
        days: Optional[int] = None,
        hours: Optional[int] = None,
        minutes: Optional[int] = None,
        seconds: Optional[int] = None,
    ):
        date = date + relativedelta(years=years or 0)
        date = date + relativedelta(months=months or 0)
        date = date + relativedelta(days=days or 0)
        date = date + relativedelta(hours=hours or 0)
        date = date + relativedelta(minutes=minutes or 0)
        date = date + relativedelta(seconds=seconds or 0)
        return date
