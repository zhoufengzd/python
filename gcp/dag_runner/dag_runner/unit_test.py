import datetime

from dag_runner.datetime_param import DateTimeParam


def _test_dt_param():
    dtParam = DateTimeParam()
    dt = datetime.datetime.now()
    for dt_fmt in DateTimeParam.DATE_FMT:
        dt_str = dt.strftime(dt_fmt)
        print("{} => {}".format(dt_str, str(DateTimeParam.parse_date(dt_str))))

    tm_windows = ["2018-01-01:2018-02-01", "20180101-20180201", "30d", "1m", "6m", "1y"]
    for tw in tm_windows:
        print("{} => {}".format(tw, str(DateTimeParam.parse_time_window(tw))))

    dt_params = ["{{ today }}", "{{ yesterday }}", "{{ 30_days_ago }}", "{{ 180_days_ago }}", "{{ 4_months_ago }}", "{{ 3_months_ago }}", "{{ 16_months_ago }}"]
    for dp in dt_params:
        print("{} => {}, {}".format(dp, str(dtParam.to_date(dp)), str(dtParam.to_date(dp, "%Y-%m-01"))))


if __name__ == "__main__":
    _test_dt_param()
