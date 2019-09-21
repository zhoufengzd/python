import datetime


class DateTimeParam:
    """ Support:
            1. parse date time string with a few format
            2. parse time window string flexible format, and date delta
            3. predefined tags:
                {{ today }}, {{ yesterday }}, {{ tomorrow }}, {{ n_days_ago }}, {{ n_months_ago }}
    """
    DATE_FMT = ["%Y-%m-%d", "%Y%m%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S+00",
                "%Y-%m-%d %H:%M:%S.%f", "%m/%d/%y %H:%M:%S", "%m/%d/%y %H:%M", "%m/%d/%y %I:%M %p", "%Y%m%d_%H%M%S"]

    @staticmethod
    def parse_date(dt):
        """
        :param time_window: free format date string or datetime variable
        :return: datetime variable
        """
        if type(dt) is datetime.datetime:
            return dt

        str_date = str(dt).replace("T", " ")
        for dt_fmt in DateTimeParam.DATE_FMT:
            try:
                return datetime.datetime.strptime(str(str_date), dt_fmt)
            except:
                pass
        return None

    @staticmethod
    def parse_time_window(time_window):  ## 2018-01-01:2018-02-01, 20180101-20180201, or 30d, 1m, 6m, 1y
        """
        :param time_window: free format time window string
        :return: start_date and end_date
        """
        end_date = datetime.date.today()
        start_date = None

        parts = time_window.split(" ")
        if len(parts) != 2:
            parts = time_window.split(":")
        if len(parts) != 2:
            parts = time_window.split("-")
        if len(parts) == 2:  ## 2018-01-01;2018-02-01
            start_date = DateTimeParam.parse_date(parts[0])
            end_date = DateTimeParam.parse_date(parts[1])
            return start_date, end_date

        time_window = str(time_window).upper().replace("DAY", "D").replace("MONTH", "M").replace("YEAR", "Y")
        unit = 1  ## 1 day
        if "M" in time_window:
            unit = 30
        elif "Y" in time_window:
            unit = 365
        start_date = end_date - datetime.timedelta(days=int(time_window.strip("DMY")) * unit)
        return start_date, end_date

    @staticmethod
    def parse_time_delta(time_delta):  ## d/day, w/week, m/month, y/year
        """
        :param time_unit:
        :return: normalized time unit
        """
        delta = str(time_delta).upper().replace("DAY", "D").replace("WEEK", "W").replace("MONTH", "M").replace("YEAR", "Y")
        unit = None
        if "W" in delta:
            unit = "week"
        elif "M" in delta:
            unit = "month"
        elif "Y" in delta:
            unit = "year"
        else:
            unit = "day"
        unit_count = delta.strip("DWMY")
        return [unit, int(unit_count) if unit_count else 1]

    def __init__(self):
        tm = dict()
        dt_today = datetime.date.today()
        tm["today"] = dt_today
        tm["yesterday"] = (dt_today - datetime.timedelta(days=1))
        tm["tomorrow"] = (dt_today + datetime.timedelta(days=1))
        self._dates = tm

    def to_date(self, date_param, date_format="%Y-%m-%d"):
        param = date_param.replace("{{ ", "").replace(" }}", "")
        dt = self._dates.get(param, None)
        if not dt:
            dt_today = datetime.date.today()
            if param.endswith("_days_ago"):
                n = int(param.replace("_days_ago", ""))
                dt = (dt_today - datetime.timedelta(days=n))
            elif param.endswith("_months_ago"):
                n = int(param.replace("_months_ago", ""))
                total_month = ((dt_today.year - 1900) * 12 + dt_today.month - n)
                year = total_month // 12 + 1900
                month = total_month % 12
                if month == 0:
                    month = 12
                    year -= 1
                dt = datetime.date(year, month, dt_today.day)
            self._dates[param] = dt

        if date_format:
            return dt.strftime(date_format)
        return dt
