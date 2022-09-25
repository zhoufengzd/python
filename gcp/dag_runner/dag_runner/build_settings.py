import yaml
import os

def build(config_file, app_name=None):
    config = dict()
    if not app_name:
        app_name = "demo_dag"
    app_settings = dict()
    config[app_name] = dict()
    config[app_name]["app_settings"] = app_settings

    app_settings["gcp_project"] = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("PROJECT", "test"))
    app_settings["gcs_staging"] = "gs://staging-" + app_settings["gcp_project"]
    app_settings["dag_catchup"] = False
    app_settings["start_date"] = None
    app_settings["schedule"] = None
    app_settings["templates"] = None

    params = dict()
    app_settings["params"] = params
    params["federated_query_connection"] = None

    tables = list()
    app_settings["tables"] = tables
    tables.append({"table": "mapped_table"})

    stages = list()
    app_settings["stages"] = stages
    stage = dict()
    stage["stage"] = 1
    stage["sql"] = "dummy.sql"
    stage["output"] = "bq.dummy_table"
    stage["write_disposition"] = "WRITE_TRUNCATE"
    stages.append(stage)

    with open(config_file, "w") as outf:
        yaml.dump(config, outf)


if __name__ == "__main__":
    build("test.yml")