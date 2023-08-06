import datetime
import calendar
from dateutil.relativedelta import relativedelta
from typing import List, Tuple


def pad_month_head_tail_dates(row_dates_list: List[int], selected_year: int, selected_month: int, prev: bool = True) \
        -> List[int]:
    """
    pad the head or tail dates of certain month
    """
    intended_month_fill_day_nos: int = row_dates_list.count(0)

    intended_year_month_year, intended_year_month_month = get_intended_year_month(
        selected_year, selected_month, prev)  # type: int, int
    intended_month_full_dates_num: int = calendar.monthrange(
        intended_year_month_year, intended_year_month_month)[1]
    intended_month_fill_dates: List[int] = list(range(1, intended_month_full_dates_num + 1))[
                                           -intended_month_fill_day_nos:] if prev else \
        list(range(1, intended_month_full_dates_num + 1)[:intended_month_fill_day_nos])

    if prev is False:
        intended_month_fill_dates.reverse()
        row_dates_list.reverse()

    for idx in range(intended_month_fill_day_nos):
        row_dates_list[idx] = intended_month_fill_dates[idx]

    if prev is False:
        row_dates_list.reverse()

    return row_dates_list


def get_intended_year_month(year: int, month: int, prev: bool = True) -> Tuple[int, int]:
    intended_year_month = datetime.date(
        year, month, 1) - relativedelta(months=1 if prev else -1)
    return intended_year_month.year, intended_year_month.month


def get_month_head_tail(select_year: int, select_month: int) -> List[List[int]]:
    """
    get the initial dates numbers
    """
    return calendar.monthcalendar(select_year, select_month)


def fmt_str_date(year: int, month: int, day: int) -> str:
    """
    get the formatted date like '2020-02-09' instead of '2020-2-9'
    """
    str_date_ptn = '%s'
    lt_10 = range(1, 10) 
    number_cmp = [month, day]
    
    for no in number_cmp:
        str_date_ptn += '-0%s' if no in lt_10 else '-%s'

    return str_date_ptn % (year, month, day)
