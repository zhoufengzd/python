import argparse
import os
import time
from subprocess import Popen, PIPE

from dag_runner.big_query_runner import BigQueryRunner
from dag_runner.dag_builder import DagBuilder
from dag_runner.settings import Settings


class JobExecutor:
    """ job executor. Responsible for execute all stages for a job.
     Attributes:
         done: return True if all the stages are completed.
     """
    def __init__(self, settings):
        if os.path.exists(settings):
            self._settings = Settings(settings)
        else:
            self._settings = settings
        self._done = False

    def update_settings(self):
        self.__do_execute(self._settings.stages, "stages")

    @property
    def done(self):
        return self._done

    def execute(self):
        self.__do_execute(self._settings.stages, "stages")

    def build_dag(self):
        import shutil

        st = self._settings
        dag_file = str(st.config_file).replace(".config", "").replace(".yaml", "_dag.py")
        if os.path.exists(st.dag_directory):
            shutil.rmtree(st.dag_directory)
        DagBuilder.build_dag(st.app_name, st, os.path.join(st.dag_directory, dag_file), schedule_interval=st.schedule, start_date=st.start_date)

    def __do_execute(self, stages, stage_tag):
        import shutil

        self._done = False
        if not stages:
            self._done = True
            return

        settings = self._settings
        sql_env, sql_keyword_map = DagBuilder.build_jinja_env(settings, settings.table_map_local, settings.time_map, settings.params_local)
        stage_directory = os.path.join(settings.generated_directory, "local", settings.app_name, stage_tag)
        if os.path.exists(stage_directory):
            shutil.rmtree(stage_directory)
        for stage_id in sorted(stages):  # sort by stage id
            steps = stages[stage_id]
            jobs = []
            for step in steps:
                if step.get("sql", None):
                    self.__run_bq_job(step, stage_id, stage_directory, sql_keyword_map, sql_env, settings, jobs)
                elif step.get("bash", None):
                    self.__run_bash_job(step["bash"])
                else:
                    raise Exception("Error! Only sql and bash steps are supported!")
            # check queries of a stage are done and move to the next stage
            while True:
                jobs_running = len(jobs)
                for job in jobs:
                    if job.done:
                        jobs_running -= 1
                if jobs_running == 0:
                    break
                time.sleep(5)
        self._done = True

    def __run_bq_job(self, step, stage_id, stage_directory, sql_keyword_map, sql_env, global_settings, jobs):
        job = BigQueryRunner(global_settings.project, global_settings.dataset, quiet=global_settings.quiet)
        jobs.append(job)
        step_output_dir = os.path.join(stage_directory, str(stage_id))

        step_filter = sql_keyword_map.copy()
        step_filter.update(step.get("params", dict()))

        check = step.get("check", None)
        if check is not None:  # 0 could be a valid check
            result = job.fetch_one(DagBuilder.process_template(step["sql"], step_filter, step_output_dir, sql_env))
            if result is None or result == False:
                raise Exception("Error! check failed: " + str(stage_id) + " - " + step["sql"])
            if isinstance(check, (int, float)) and result[0] != check:
                raise Exception("Error! check failed: " + str(stage_id) + " - " + step["sql"] + " = " + str(result))
        else:
            job.execute(DagBuilder.process_template(step["sql"], step_filter, step_output_dir, sql_env),
                        destination_table=self.__map_output_table(step.get("output", None), self._settings.table_map_local),
                        write_disposition=step["write_disposition"])

    def __map_output_table(self, str_output_tbl, table_map):
        if not str_output_tbl:
            return None

        replaced = str_output_tbl
        for key, value in table_map.items():
            if not isinstance(value, dict):
                replaced = replaced.replace("{{ " + key + " }}", value)
        return replaced

    def __run_bash_job(self, bash_cmd):
        sp = Popen(['bash', bash_cmd], stdout=PIPE, stderr=PIPE)
        stdout, stderr = sp.communicate()
        sp.wait()
        if sp.returncode:
            raise Exception("Bash command failed\n" + stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action",
                        help="run | build. run will complete all the tasks. build will write dag file. ")
    parser.add_argument("config_file")
    args = parser.parse_args()

    et = JobExecutor(args.config_file)
    if args.action == "run":
        et.execute()
    else:
        et.build_dag()
