import datetime
import calendar
from dateutil.relativedelta import relativedelta
from typing import List, Tuple


def monthcalendar(select_year: int, select_month: int) -> List[List[int]]:
    target_fmt_date_list: List[List[int]] = get_month_head_tail(select_year, select_month)

    first_row_dates, last_row_dates = target_fmt_date_list[0], target_fmt_date_list[-1]

    target_fmt_date_list[0] = pad_month_head_tail_dates(
        first_row_dates, select_year, select_month, True)
    target_fmt_date_list[-1] = pad_month_head_tail_dates(
        last_row_dates, select_year, select_month, False)

    return target_fmt_date_list


def str_dates(select_year: int, select_month: int) -> List[str]:
    """
    get the 5*7 full month of string dates format
    """

    target_fmt_date_list: List[List[int]] = monthcalendar(
        select_year, select_month)

    # 构建查询日期列表
    cur_month_all_days_lst = [fmt_str_date(select_year, select_month, day_no) for day_no in
                              range(calendar.monthrange(select_year, select_month)[1] + 1)[1:]]

    last_month_year, last_month_month = get_intended_year_month(
        select_year, select_month, True)
    next_month_year, next_month_month = get_intended_year_month(
        select_year, select_month, False)

    last_month_dates_lst = [fmt_str_date(last_month_year, last_month_month, day_no) for day_no in
                            target_fmt_date_list[0][:target_fmt_date_list[0].index(1)]]
    
    try:
        next_month_dates_lst = [fmt_str_date(next_month_year, next_month_month, day_no) for day_no in
                                target_fmt_date_list[-1][target_fmt_date_list[-1].index(1):]]
    except ValueError:
        next_month_dates_lst = []

    calendar_all_dates_lst = []
    calendar_all_dates_lst.extend(last_month_dates_lst)
    calendar_all_dates_lst.extend(cur_month_all_days_lst)
    calendar_all_dates_lst.extend(next_month_dates_lst)

    return calendar_all_dates_lst


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
