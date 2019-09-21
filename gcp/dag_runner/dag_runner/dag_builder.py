import codecs
import datetime
import os
import os.path

from jinja2 import Environment, FileSystemLoader
from jinja2 import DebugUndefined, Template


class DagBuilder:
    DAG_HEADER_FILE = "dag_header_py"

    STAGE_MARK_OPERATOR_TEMPLATE = """\
{{ op_instance }}=BashOperator(task_id=\"{{ op_instance }}\", bash_command=\"echo \\\"{{ op_instance }} is completed.\\\"\",dag=dag)
"""
    BIGQUERY_OPERATOR_TEMPLATE = """\
{{ op_instance }}=BigQueryOperator(task_id=\"{{ task_name }}\",
                    sql=\"{{ sql_file }}\",
                    destination_dataset_table=\"{{ output_table }}\",
                    write_disposition=\"{{ write_disposition }}\",
                    bigquery_conn_id=\"{{ bq_connection_id }}\",
                    use_legacy_sql=False,
                    dag=dag)
"""
    BIGQUERY_OPERATOR_NO_WRITE_TEMPLATE = """\
{{ op_instance }}=BigQueryOperator(task_id=\"{{ task_name }}\",
                    sql=\"{{ sql_file }}\",
                    bigquery_conn_id=\"{{ bq_connection_id }}\",
                    use_legacy_sql=False,
                    dag=dag)
"""
    BIGQUERY_CHECKOPERATOR_TEMPLATE = """\
{{ op_instance }}=BigQueryCheckOperator(task_id=\"{{ task_name }}\",
                    sql=\"{{ sql }}\",
                    bigquery_conn_id=\"{{ bq_connection_id }}\",
                    use_legacy_sql=False,
                    dag=dag)
"""
    BIGQUERY_VALUECHECKOPERATOR_TEMPLATE = """\
{{ op_instance }}=BigQueryValueCheckOperator(task_id=\"{{ task_name }}\",
                    sql=\"{{ sql }}\",
                    bigquery_conn_id=\"{{ bq_connection_id }}\",
                    pass_value={{ pass_value }},
                    use_legacy_sql=False,
                    dag=dag)
"""
    BASH_OPERATOR_TEMPLATE = """\
{{ op_instance }}=BashOperator(task_id=\"{{ op_instance }}\", bash_command=\"{{ bash_file }}\",dag=dag)
"""
    DAG_TRIGGER_OPERATOR_TEMPLATE = """\
{{ op_instance }}=TriggerDagRunOperator(task_id=\"{{ task_name }}\",
                    trigger_dag_id=\"{{ dag_triggered }}\",
                    python_callable=on_trigger,
                    params={'condition_param': True, 'message': '{{ dag_triggered }} is trigged'},
                    dag=dag)
"""
    DAG_EXECUTE_OPERATOR_TEMPLATE = """\
{{ op_instance }}=ExecuteDagRunOperator(task_id=\"{{ task_name }}\",
                    execute_dag_id=\"{{ dag_execute }}\",
                    python_callable=on_trigger,
                    params={'condition_param': True, 'message': '{{ dag_triggered }} is trigged'},
                    dag=dag)
"""

    DOWNSTREAM_TEMPLATE = "{{ task_id }} >> ({{ next_task_id }})"
    UPSTREAM_TEMPLATE = "{{ prev_task_id }} >> {{ task_id }}"

    DAG_FOOTER = """\
if __name__ == \"__main__\":
    dag.cli()"""

    @staticmethod
    def build_jinja_env(settings, tablemap, time_map, params, template_directories=None):
        if not template_directories:
            template_directories = DagBuilder._get_template_directories(settings.template_directories)

        sql_env = Environment(loader=FileSystemLoader(template_directories))
        sql_keyword_map = dict()
        sql_keyword_map.update(tablemap)
        sql_keyword_map.update(time_map)
        sql_keyword_map.update(params)

        sql_keyword_map["gcp_project"] = settings.project
        sql_keyword_map["gcp_dataset"] = settings.dataset

        return sql_env, sql_keyword_map

    @staticmethod
    def build_dag(dag_id, settings, dag_file, schedule_interval, start_date=None):
        """ build dag from configurations.
        :param dag_file:
        :return:
        """
        tasks = []
        stage_marks = []
        all_sequences = []
        template_directories = DagBuilder._get_template_directories(settings.template_directories)
        sql_env, sql_keyword_map = DagBuilder.build_jinja_env(settings, settings.table_map_airflow, settings.time_map, settings.params_airflow, template_directories)
        dag_header = DagBuilder.build_dag_header(dag_id, schedule_interval if schedule_interval else "", start_date if start_date else "",
                                                 settings.dag_catchup, template_directories)

        DagBuilder.__build_tasks(settings, "stages", None, sql_env, sql_keyword_map, all_sequences, tasks, stage_marks)
        with open(dag_file, "w") as of:
            of.write(dag_header)
            of.write("\n\n")
            of.write("## stages: ---------------------------------------------------------\n")
            for s in stage_marks:
                of.write(s + "\n")
            of.write("\n\n")
            of.write("## tasks: ---------------------------------------------------------\n")
            for t in tasks:
                of.write(t + "\n")
            of.write("\n\n")
            of.write("## task sequences: ------------------------------------------------\n")
            for sq in all_sequences:
                of.write(sq + "\n")
            of.write("\n\n")
            of.write(DagBuilder.DAG_FOOTER)

    @staticmethod
    def __build_tasks(settings, stage_group, prev_stage, sql_env, sql_keyword_map, all_sequences, tasks, stage_marks):
        """ build dag tasks from configurations."""
        stages = settings.stages
        generated_dir = os.path.join(settings.generated_directory, "airflow", settings.app_name, stage_group)
        table_map = settings.table_map_airflow

        task_idx = len(tasks)
        current_stage = None
        for stage_id in sorted(stages):  # sort by stage id
            steps = stages[stage_id]
            upstreams = []
            dnstreams = []
            current_stage = DagBuilder.to_stage_instance(stage_group, stage_id)
            stage_marks.append(DagBuilder.build_stage_mark_operator(current_stage))
            for step in steps:
                if step.get("sql", None):
                    step_filter = sql_keyword_map.copy()
                    step_filter.update(step.get("params", dict()))
                    sql_file = DagBuilder.process_template(step["sql"], step_filter,
                                                           os.path.join(generated_dir, str(stage_id)), sql_env)

                    output_table = None
                    if step.get("output", None):
                        output_table = DagBuilder.process_table_map(step["output"], table_map)

                    task = DagBuilder.build_bq_operator(settings.dag_directory, task_idx,
                                                        sql_file=sql_file,
                                                        output_table=output_table,
                                                        write_disposition=step.get("write_disposition", None),
                                                        check=step.get("check", None),
                                                        stage_id=stage_id)
                elif step.get("bash", None):
                    task = DagBuilder.build_bash_operator(task_idx, bash_file=step["bash"], stage_id=stage_id)
                elif step.get("dag_triggered", None):
                    task = DagBuilder.build_dag_trigger_operator(task_idx, dag_triggered=step["dag_triggered"], stage_id=stage_id)
                elif step.get("dag_execute", None):
                    task = DagBuilder.build_dag_execute_operator(task_idx, dag_execute=step["dag_execute"], stage_id=stage_id)

                tasks.append(task)
                dnstreams.append(DagBuilder.build_downstream(task_idx, current_stage))  # point to the end of this stage
                if prev_stage:  # point upstream to previous stage
                    upstreams.append(DagBuilder.build_upstream(task_idx, prev_stage))
                task_idx += 1

            prev_stage = current_stage
            all_sequences.extend(upstreams)
            all_sequences.extend(dnstreams)
        return current_stage

    @staticmethod
    def process_template(template_file, jinja_parameters, output_dir, jinja_env=None):
        """process templated query
        :param step: a dictionary containing info to process a jinja templated query
        """
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        generated_file = os.path.join(output_dir, template_file)

        if not jinja_env:
            search_dirs = [os.path.dirname(os.path.abspath(__file__)), os.path.dirname(template_file)]
            jinja_env = Environment(loader=FileSystemLoader(search_dirs))

        with codecs.open(generated_file, "w", encoding="utf-8") as of:
            of.write(jinja_env.get_template(template_file).render(jinja_parameters))
        return generated_file

    @staticmethod
    def process_table_map(template_string, table_map):
        """process templated string"""
        replaced = template_string
        for key, value in table_map.items():
            if not isinstance(value, dict):
                replaced = replaced.replace("{{ " + key + " }}", value)
        return replaced

    @staticmethod
    def build_dag_header(dag_id, schedule="", start_date=None, dag_catchup=False, template_directories=None):
        """
        :param dag_template_file: dag header template file
        :param dag_start_date: if not set, default to start from yesterday
        :return: dag header string
        """
        header_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), DagBuilder.DAG_HEADER_FILE)
        with open(header_file, "r") as f:
            header_template = f.read()
        keywords = {"dag_id": dag_id, "schedule": schedule, "start_date": start_date, "dag_catchup": dag_catchup, "search_diretories": ""}
        return Template(header_template, undefined=DebugUndefined).render(keywords)

    @staticmethod
    def build_bq_operator(dag_dir, task_id, sql_file, output_table=None, write_disposition="WRITE_TRUNCATE",
                          check=None, task_name=None, stage_id=None):
        """
        :param task_id: task instance id
        :param sql_file: sql file for airflow BigQueryOperator
        :param output_table: output table
        :param write_disposition: truncate or append
        :param check: if defined, will build bigquery check operator instead
        :param task_name: a friendly task name
        :param stage_id: stage id if multiple tasks share the same stage
        :return: string of BigQueryOperator instance initialization
        """
        filename_base = os.path.splitext(os.path.basename(sql_file))[0]
        if not task_name:
            # task_name = 'stage{:02d}_{:s}_{:s}'.format(int(stage_id if stage_id else task_id), str(task_id),
            #                                            filename_base.replace("-", "_"))
            task_name = filename_base.replace("-", "_")

        bq_connection_id = "google_cloud_default"
        if check:
            if not isinstance(check, bool) and isinstance(check, (int, float)):
                t = Template(DagBuilder.BIGQUERY_VALUECHECKOPERATOR_TEMPLATE);
            else:
                t = Template(DagBuilder.BIGQUERY_CHECKOPERATOR_TEMPLATE);
            kwds = {"op_instance": DagBuilder.to_task_instance(task_id), "sql": DagBuilder.__read_sql_file(sql_file),
                    "pass_value": check, "bq_connection_id": bq_connection_id, "task_name": task_name}
        else:
            t = Template(DagBuilder.BIGQUERY_OPERATOR_TEMPLATE if output_table else DagBuilder.BIGQUERY_OPERATOR_NO_WRITE_TEMPLATE);
            kwds = {"op_instance": DagBuilder.to_task_instance(task_id), "sql_file": sql_file.replace(dag_dir + "/", ""),
                    "output_table": output_table,
                    "write_disposition": write_disposition, "bq_connection_id": bq_connection_id,
                    "task_name": task_name}
        return t.render(kwds)

    @staticmethod
    def build_bash_operator(task_id, bash_file, task_name=None, stage_id=None):
        """
        :param task_id: task instance id
        :param bash_file: bash file for airflow BashOperator
        :param task_name: a friendly task name
        :param stage_id: stage id if multiple tasks share the same stage
        :return: string of BashOperator instance initialization
        """
        filename_base = os.path.splitext(os.path.basename(bash_file))[0]
        if not task_name:
            task_name = 'stage{:02d}_{:s}_{:s}'.format((stage_id if stage_id else task_id), str(task_id),
                                                       filename_base.replace("-", "_"))
        t = Template(DagBuilder.BASH_OPERATOR_TEMPLATE);
        kwds = {"op_instance": DagBuilder.to_task_instance(task_id), "bash_file": bash_file, "task_name": task_name}
        return t.render(kwds)

    @staticmethod
    def build_dag_trigger_operator(task_id, dag_triggered, task_name=None, stage_id=None):
        """
        :param task_id: task instance id
        :param dag_triggered: trigger_dag_id for airflow TriggerDagRunOperator
        :param task_name: a friendly task name
        :param stage_id: stage id if multiple tasks share the same stage
        :return: string of BashOperator instance initialization
        """
        if not task_name:
            task_name = 'stage{:02d}_{:s}_trigger_{:s}'.format((stage_id if stage_id else task_id), str(task_id),
                                                       dag_triggered.replace("-", "_"))
        t = Template(DagBuilder.DAG_TRIGGER_OPERATOR_TEMPLATE);
        kwds = {"op_instance": DagBuilder.to_task_instance(task_id), "dag_triggered": dag_triggered, "task_name": task_name}
        return t.render(kwds)

    @staticmethod
    def build_dag_execute_operator(task_id, dag_execute, task_name=None, stage_id=None):
        """
        :param task_id: task instance id
        :param dag_execute: executed_dag_id for airflow ExecuteDagOperator
        :param task_name: a friendly task name
        :param stage_id: stage id if multiple tasks share the same stage
        :return: string of BashOperator instance initialization
        """
        if not task_name:
            task_name = 'stage{:02d}_{:s}_trigger_{:s}'.format((stage_id if stage_id else task_id), str(task_id),
                                                       dag_execute.replace("-", "_"))
        t = Template(DagBuilder.DAG_EXECUTE_OPERATOR_TEMPLATE);
        kwds = {"op_instance": DagBuilder.to_task_instance(task_id), "dag_execute": dag_execute, "task_name": task_name}
        return t.render(kwds)

    @staticmethod
    def build_stage_mark_operator(op_instance):
        """
        :param stage_id: task tage id
        :return: string of BashOperator instance as end of the stage mark
        """
        t = Template(DagBuilder.STAGE_MARK_OPERATOR_TEMPLATE);
        return t.render({"op_instance": op_instance})

    @staticmethod
    def build_downstream(task_id, next_task_id):
        """
        :param step_id: step id in dag
        :return: string of sequence of task and prev task
        """
        t = Template(DagBuilder.DOWNSTREAM_TEMPLATE);
        return t.render({"task_id": DagBuilder.to_task_instance(task_id),
                         "next_task_id": DagBuilder.to_task_instance(next_task_id)})

    @staticmethod
    def build_upstream(task_id, prev_task_id):
        """
        :param step_id: step id in dag
        :return: string of sequence of task and prev task
        """
        t = Template(DagBuilder.UPSTREAM_TEMPLATE);
        return t.render({"task_id": DagBuilder.to_task_instance(task_id),
                         "prev_task_id": DagBuilder.to_task_instance(prev_task_id)})

    @staticmethod
    def to_task_instance(task_id):
        return "t" + str(task_id) if DagBuilder._all_digits(task_id) else str(task_id)

    @staticmethod
    def to_stage_instance(stage_group, stage_id):
        return stage_group + str(stage_id)

    @staticmethod
    def _all_digits(str_value):
        for c in str(str_value):
            if not c.isdigit():
                return False
        return True

    @staticmethod
    def _get_template_directories(template_directories):
        template_dirs = []
        for tpl_dir in template_directories:
            for sub_dir in os.walk(tpl_dir, followlinks=True):
                template_dirs.append(sub_dir[0])
        return template_dirs

    @staticmethod
    def _find_file(file_name, search_directories):
        for sd in search_directories:
            file_path = os.path.join(sd, file_name)
            if os.path.isfile(file_path):
                return file_path
        return None

    @staticmethod
    def __read_sql_file(sql_file):
        query = ""
        with open(sql_file) as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("--"):  # skip comment lines
                    query += line + " "
        return query
