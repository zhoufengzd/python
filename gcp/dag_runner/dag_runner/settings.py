import datetime
import os

import yaml
from jinja2 import DebugUndefined, Template


class Settings:
    @staticmethod
    def parse_date(dt):
        if type(dt) is datetime.datetime:
            return dt

        str_date = str(dt)
        supported_date_fmt = ["%Y-%m-%d", "%Y%m%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S+00", "%Y-%m-%d %H:%M:%S.%f",
                              "%m/%d/%y %H:%M:%S", "%m/%d/%y %H:%M", "%m/%d/%y %I:%M %p"]
        str_date = str_date.replace("T", " ")
        for dt_fmt in supported_date_fmt:
            try:
                return datetime.datetime.strptime(str(str_date), dt_fmt)
            except:
                pass
        return None

    @staticmethod
    def parse_time_window(time_window):  ## 2018-01-01;2018-02-01, or 30d, 1m, 6m, 1y
        """
        :param time_window: free format time window string
        :return: start_date and end_date
        """
        end_date = datetime.date.today()
        start_date = None

        parts = time_window.split(",")
        if len(parts) == 2:  ## 2018-01-01;2018-02-01
            start_date = Settings.parse_date(parts[0])
            end_date = Settings.parse_date(parts[1])
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

    def __init__(self, config_file, app_name=None):
        self._config_file = config_file
        self._read_config(app_name)

    @property
    def config_file(self):
        return self._config_file

    @property
    def app_name(self):
        return self._app_name

    @property
    def code_directory(self):
        return self._current_dir

    @property
    def project(self):
        return self._project

    @property
    def dataset(self):
        return self._dataset

    @property
    def gcs_temp(self):
        return self._gcs_temp

    @property
    def gcs_staging(self):
        return self._gcs_staging

    @property
    def quiet(self):
        return self._quiet

    @property
    def dag_catchup(self):
        return self._dag_catchup

    @property
    def schedule(self):
        return self._schedule

    @property
    def start_date(self):
        return self._start_date

    @property
    def query_config(self):
        return self._query_config

    @property
    def template_directories(self):
        return self._template_dirs

    @property
    def generated_directory(self):
        return self._generated_dir

    @property
    def dag_directory(self):
        return os.path.join(self._generated_dir, "airflow", self._app_name)

    @property
    def table_map_local(self):
        """fully interpreted table map"""
        tbl_map = dict()

        dt_map = dict()
        dt_map["project"] = self._project
        dt_map["start_date_label"] = self._time_map["start_date_label"]
        dt_map["end_date_label"] = self._time_map["end_date_label"]
        dt_map["end_datetime_label"] = self._time_map["end_datetime_label"]
        dt_map["ds"] = self._time_map["end_date"]
        dt_map["ds_nodash"] = self._time_map["end_date_label"]
        dt_map["yesterday_ds"] = self._time_map["yesterday"]
        dt_map["yesterday_ds_nodash"] = self._time_map["yesterday"].replace("-", "")
        for key, value in self._table_map.items():
            tbl_map[key] = value
            if not isinstance(value, dict) and value.find("{") > -1:    # leave unknown templates as they are
                tbl_map[key] = Template(value, undefined=DebugUndefined).render(dt_map);
        return tbl_map

    @property
    def table_map_airflow(self):
        """partially interpreted table map. airflow tags were left intact."""
        tbl_map = dict()

        dt_map = dict()
        dt_map["project"] = self._project
        dt_map["start_date_label"] = self._time_map["start_date_label"]
        dt_map["end_date_label"] = self._time_map["end_date_label"]
        dt_map["end_datetime_label"] = self._time_map["end_datetime_label"]
        for key, value in self._table_map.items():
            tbl_map[key] = value
            if isinstance(value, dict):
                print("aha, dictionary table map!")

            if not isinstance(value, dict) and value.find("{") > -1:    # leave unknown templates as they are
                tbl_map[key] = Template(value, undefined=DebugUndefined).render(dt_map);
        return tbl_map

    @property
    def params_local(self):
        params = dict()
        params.update(self._params)
        params["ds"] = self._time_map["end_date"]
        params["ds_nodash"] = self._time_map["end_date_label"]
        params["yesterday_ds"] = self._time_map["yesterday"]
        params["yesterday_ds_nodash"] = self._time_map["yesterday"].replace("-", "")
        return params

    @property
    def params_airflow(self):
        params = dict()
        params.update(self._params)
        params["ds"] = "{{ ds }}"
        params["ds_nodash"] = "{{ ds_nodash }}"
        params["yesterday_ds"] = "{{ yesterday_ds }}"
        params["yesterday_ds_nodash"] = "{{ yesterday_ds_nodash }}"
        return params

    @property
    def stages(self):
        return self._stages

    @property
    def time_map(self):
        return self._time_map

    def update_time_map(self, start_date, end_date, time_delta=None):
        tm = dict()
        dt_today = datetime.date.today()
        tm["time_delta"] = time_delta
        if not tm["time_delta"]:
            tm["time_delta"] = ["day", 1]
        tm["day_interval"] = tm["time_delta"][1]
        tm["today"] = dt_today.strftime('%Y-%m-%d')
        tm["yesterday"] = (dt_today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        tm["tomorrow"] = (dt_today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        tm["dag_start_date"] = tm["yesterday"]

        ## data start / end timestamp
        dt_end = dt_today
        if end_date:
            dt_end = Settings.parse_date(end_date)
        dt_start = dt_end - datetime.timedelta(days=1)
        if start_date:
            dt_start = Settings.parse_date(start_date)
        tm["start_timestamp"] = dt_start.strftime("%Y-%m-%d %H:%M:%S")
        tm["end_timestamp"] = dt_end.strftime("%Y-%m-%d %H:%M:%S")
        tm["start_date"] = dt_start.strftime("%Y-%m-%d")
        tm["start_date_label"] = dt_start.strftime("%Y%m%d")
        tm["end_date"] = dt_end.strftime("%Y-%m-%d")
        tm["end_date_label"] = dt_end.strftime("%Y%m%d")
        tm["end_datetime_label"] = dt_end.strftime("%Y%m%d_%H%M%S")

        # summary
        tm["thirty_days_ago"] = (dt_today - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        tm["ninety_days_ago"] = (dt_today - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
        tm["one_eighty_days_ago"] = (dt_today - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
        tm["one_year_ago"] = (dt_today - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self._time_map = tm

    def _read_config(self, app_name=None):
        with open(self._config_file, 'r') as yf:
            config = yaml.load(yf.read(), Loader=yaml.BaseLoader)

        self._app_name = app_name if app_name else list(config.keys())[0]
        app_settings = config.get(self._app_name).get("app_settings")

        self._current_dir = os.path.dirname(os.path.abspath(__file__))
        self._project = app_settings.get("gcp_project", os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("PROJECT", "test")))
        self._gcs_staging = app_settings.get("gcs_staging", "gs://staging-" + self._project + "/" + self._app_name + "/staging")
        self._gcs_temp = app_settings.get("gcs_temp", "gs://staging-" + self._project + "/" + self._app_name + "/temp")
        self._dataset = app_settings.get("gcp_dataset")

        self._quiet = app_settings.get("quiet")
        self._dag_catchup = app_settings.get("dag_catchup", False)
        self._template_dirs = app_settings.get("templates", "templates").split(";")
        self._generated_dir = app_settings.get("generated", "_generated")
        self._schedule = app_settings.get("schedule", None)
        self._start_date = app_settings.get("start_date", None)

        bq_settings = app_settings.get("bq_settings")
        self._query_config = dict()
        self._query_config["allow_large_results"] = bq_settings.get("allow_large_results", True) if bq_settings else True
        self._query_config["use_legacy_sql"] = bq_settings.get("use_legacy_sql", False) if bq_settings else True

        self._params = app_settings.get("params", dict())

        self._table_map = dict()
        self._table_map.update(app_settings.get("tables", dict()))

        self._stages = self._build_stages(app_settings.get("stages"))
        self.update_time_map(None, None)

    def _build_stages(self, stage_settings):
        stages = dict()
        if not stage_settings:
            return stages

        for stage in stage_settings:
            stage_id = int(stage["stage"])

            steps = stages.get(stage_id)
            if not steps:
                steps = []
                stages[stage_id] = steps
            steps.append(stage)

            if not stage.get("write_disposition", None):
                stage["write_disposition"] = "WRITE_TRUNCATE"
        return stages
