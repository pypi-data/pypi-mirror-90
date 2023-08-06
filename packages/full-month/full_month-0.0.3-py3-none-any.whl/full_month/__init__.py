import calendar
from typing import List

from date_handler import pad_month_head_tail_dates, get_intended_year_month, get_month_head_tail, fmt_str_date


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
