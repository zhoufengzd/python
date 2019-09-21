#!/usr/bin/env python

import argparse
import json
import os
import re
import time

from google.cloud import bigquery
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.job import QueryJobConfig, CopyJobConfig, ExtractJobConfig, LoadJobConfig
from google.cloud.bigquery.table import TableReference


class DtTblRef:
    @staticmethod
    def default_project():
        project = os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project:
            raise EnvironmentError("Error! Default GCP_PROJECT or GOOGLE_CLOUD_PROJECT is not set. ")
        return project

    def __init__(self, table_name=None, dataset_name=None, project_name=None):
        """ table name: [project.][dataset.]table. could be tbl_*_sth, or tbl_[min-max] for table names in range """
        self.project = project_name
        self.dataset = dataset_name
        self.table = table_name
        self.table_min = None  # to qualify date partitioned table, table min name
        self.table_max = None  # table max name

        if table_name:
            name_parts = table_name.replace(":", ".").split(".")
            if len(name_parts) == 3:  # project.dataset.table
                self.project = name_parts[0]
                self.dataset = name_parts[1]
                self.table = name_parts[2]
            elif len(name_parts) == 2:  # dataset.table
                self.dataset = name_parts[0]
                self.table = name_parts[1]

            tbl_parts = self.table.split("[")
            if len(tbl_parts) == 2:
                self.table = tbl_parts[0]
                dt_parts = tbl_parts[1].rstrip("]").split("-")
                self.table_min = self.table.rstrip("*") + dt_parts[0] if dt_parts[0] else None
                self.table_max = self.table.rstrip("*") + dt_parts[1] if dt_parts[1] else None

        if not self.project:
            self.project = DtTblRef.default_project()
        self.dataset_ref = DatasetReference(dataset_id=self.dataset, project=self.project)
        self.table_ref = TableReference(dataset_ref=self.dataset_ref, table_id=self.table)

    def __str__(self):
        return "{}.{}.{}".format(self.project or "?", self.dataset or "?", self.table or "?")


class BQUtil:
    def __init__(self, project=None):
        self._connections = dict()
        self._project = project or DtTblRef.default_project()

    def get_datasets(self, dt_ref):
        dt_pattern = dt_ref.dataset.replace("*", ".+")
        if ".+" not in dt_pattern:
            return [dt_pattern]

        datasets = []
        for dt in self.connect(dt_ref.project).list_datasets(include_all=True):
            if re.search(dt_pattern, dt.dataset_id):
                datasets.append(dt.dataset_id)
        return datasets

    def get_tables(self, tbl_ref, types=['TABLE']):
        """ return table names for this table ref / dataset.table_patterns """
        tbl_pattern = tbl_ref.table.replace("*", ".+")
        if ".+" not in tbl_pattern:
            return [tbl_pattern]

        tables = []
        for tbl in self.connect(tbl_ref.project).list_tables(dataset=tbl_ref.dataset_ref):
            # print(tbl.table_id)
            if not tbl.table_type in types:
                continue
            if tbl_pattern and not re.search(tbl_pattern, tbl.table_id):
                continue
            if tbl_ref.table_min and tbl.table_id < tbl_ref.table_min:
                continue
            if tbl_ref.table_max and tbl.table_id >= tbl_ref.table_max:
                continue

            tables.append(tbl.table_id)
        return tables

    def delete(self, tbl_ref, preview):
        datasets = self.get_datasets(tbl_ref)
        for dt in datasets:
            tables = self.get_tables(DtTblRef(tbl_ref.table, dt, tbl_ref.project), types=['TABLE', 'VIEW'])
            for tbl in tables:
                print("--  {}delete {}.{} ".format("preview: " if preview else "", dt, tbl))
                if preview:
                    continue
                self.connect(tbl_ref.project).delete_table(TableReference(tbl_ref.dataset_ref, tbl))

    def mirror(self, tgt_ref, src_ref, preview=True):
        MAP_VIEW_SQL_FMT = "create or replace view {}.{} as \n\tselect * from `{}.{}.{}`"

        tables = BQUtil().get_tables(src_ref)
        tgt_client = BQUtil(tgt_ref.project)
        for tbl in tables:
            map_sql = MAP_VIEW_SQL_FMT.format(tgt_ref.dataset, tbl, src_ref.project, src_ref.dataset, tbl)
            tgt_client.execute(map_sql, preview=preview)

    def copy(self, tgt_ref, src_ref, append=False, preview=True):
        jc = CopyJobConfig()
        jc.create_disposition = "CREATE_IF_NEEDED"
        jc.write_disposition = "WRITE_APPEND" if append else "WRITE_TRUNCATE"

        jobs = list()
        tgt_client = BQUtil(tgt_ref.project)
        tables = BQUtil().get_tables(src_ref)
        for tbl in tables:
            src_ref = DtTblRef(tbl, src_ref.dataset, src_ref.project)
            tgt_ref = DtTblRef(tbl, tgt_ref.dataset, tgt_ref.project)
            print("--  {}{} => {} ".format("preview: " if preview else "", str(src_ref), str(tgt_ref)))
            if preview:
                continue

            jobs.append(tgt_client.connect().copy_table(src_ref.table_ref, tgt_ref.table_ref, job_config=jc))
        self.__check_jobs(jobs)

    def export(self, tbl_ref, gcs_base_dir, file_format="csv", compression=None, preview=True):
        """
        :param gcs_base_dir: gcs base bucket
        :param file_format: (Optional) csv, json or avro. default to csv if can't be determined from export_uri
        :param compression: default to None. could be gzip.
        """
        tables = self.get_tables(tbl_ref)
        jobs = list()
        jc = ExtractJobConfig()
        jc.compression = compression
        jc.destination_format = self.__get_bq_format(file_format)
        for tbl in tables:
            gcs_uri = "{}/{}/*.{}".format(gcs_base_dir, tbl, file_format)
            table_ref = TableReference(dataset_ref=tbl_ref.dataset_ref, table_id=tbl)
            print("--  {}{} => {} ".format("preview: " if preview else "", tbl, gcs_uri))
            if preview:
                continue

            jobs.append(self.connect(tbl_ref.project).extract_table(table_ref, gcs_uri, job_config=jc))
        self.__check_jobs(jobs)

    def load(self, tbl_ref, gcs_uri, file_format="csv", schema_file=None, append=False, preview=True):
        """
        table=gs://.../table/*.json to load a single table,
        or tables=gs://.../table_base_dir to load multiple tables
        """
        tables = self.get_tables(tbl_ref)
        jc, fmt = self.__build_load_config(gcs_uri, file_format, schema_file, append)
        if len(tables) > 1:
            self.__load_many(tbl_ref, tables, gcs_uri, fmt, jc, preview)
        else:
            self.__load_one(tbl_ref, gcs_uri, jc, preview)

    def migrate(self, tbl_ref, reference_file, gcs_base_dir, preview=True):
        file_format = "json"
        # export matched tables to gcs_base_dir
        tables = self.get_tables(tbl_ref)
        self.export(tbl_ref, gcs_base_dir, file_format, None, preview=preview)

        # import matched tables from gcs_base_dir using json schema, overwrite existing tables
        jc, fmt = self.__build_load_config(gcs_base_dir, file_format, reference_file, False)
        self.__load_many(tbl_ref, tables, gcs_base_dir, fmt, jc, preview)

    def execute(self, query, tbl_ref=None, append=False, preview=True):
        sql_query = self.__get_query(query)
        if tbl_ref:
            print("-- ## " + str(tbl_ref))
        print("{}{}".format("-- preview: \n" if preview else "", sql_query))
        if preview:
            return

        job_conf = QueryJobConfig()
        job_conf.use_legacy_sql = False
        if tbl_ref:
            job_conf.write_disposition = "WRITE_APPEND" if append else "WRITE_TRUNCATE"
            job_conf.default_dataset = tbl_ref.dataset_ref
            job_conf.destination = tbl_ref.table_ref
            job_conf.allow_large_results = True
        query_job = self.connect(tbl_ref.project if tbl_ref else None).query(sql_query, job_config=job_conf)
        if query_job.errors:
            raise Exception(query_job.errors)

    def fetch(self, query, timeout_seconds=30):
        query_job = self.connect().query(self.__get_query(query))
        if query_job.done:
            return query_job.result(timeout=timeout_seconds)
        return None

    def fetch_one(self, query, timeout_seconds=30):
        query_job = self.connect().query(self.__get_query(query))
        if query_job.done:
            rows = query_job.result(timeout=timeout_seconds)
            for row in rows:
                return row
        return None

    def connect(self, project=None):
        if not project:
            project = self._project

        client = self._connections.get(project, None)
        if not client:
            client = bigquery.Client(project=project)
            self._connections[project] = client
        return client

    # private functions
    def __get_query(self, query):
        if not os.path.exists(query):
            return query

        buffer = list()
        with open(query, "r") as inf:
            for line in inf:
                if not line or not line.strip() or line.startswith("--"):
                    continue
                buffer.append(line)
            return "".join(buffer)

    def __check_jobs(self, jobs):
        for job in jobs:
            while True:
                job.reload()
                if job.state == "DONE":
                    if job.error_result:
                        raise RuntimeError(job.errors)
                    break
                time.sleep(1)

    def __get_bq_format(self, raw_format):
        format_map = {"json": "NEWLINE_DELIMITED_JSON", "avro": "AVRO", "csv": "CSV"}
        return format_map.get(raw_format, "CSV")

    def __load_schema(self, schema_file):
        if not os.path.exists(schema_file):
            return None

        with open(schema_file) as data_file:
            fields_data = json.load(data_file)
        fields = list()
        for f in fields_data:
            fields.append(bigquery.SchemaField(f["name"], f["type"], mode=f.get("mode", "NULLABLE"),
                                               fields=f.get("fields", tuple())))
        return fields

    def __build_load_config(self, gcs_uri, file_format, schema_file, append):
        gcs_file_ext = os.path.splitext(gcs_uri)[1]
        if gcs_file_ext:
            file_format = gcs_file_ext.lstrip(".")

        jc = LoadJobConfig()
        jc.source_format = self.__get_bq_format(file_format)
        jc.schema = self.__load_schema(schema_file)
        jc.write_disposition = "WRITE_APPEND" if append else "WRITE_TRUNCATE"
        return jc, file_format

    def __load_one(self, tbl_ref, gcs_uri, jc, preview):
        print("--  {}{} <= {} ".format("preview: " if preview else "", str(tbl_ref), gcs_uri))
        if preview:
            return
        jobs = list()
        jobs.append(self.connect(tbl_ref.project).load_table_from_uri(gcs_uri, tbl_ref, job_config=jc))
        self.__check_jobs(jobs)

    def __load_many(self, dt_ref, tables, gcs_base_dir, file_format, jc, preview):
        """
        :param tables:
        :param gcs_base_dir: to map to table
        """
        jobs = list()
        for tbl in tables:
            data_uri = "{}/{}/*.{}".format(gcs_base_dir, tbl, file_format)
            table_ref = TableReference(dataset_ref=dt_ref.dataset_ref, table_id=tbl)
            print("--  {}{} <= {} ".format("preview: " if preview else "", tbl, data_uri))
            if preview:
                continue

            jobs.append(self.connect(dt_ref.project).load_table_from_uri(data_uri, table_ref, job_config=jc))
        self.__check_jobs(jobs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action",
                        help="< [r|run] | [mr|mirror] | [rm|remove] | [mg|migrate] | [cp|copy] | [e|export] | [i|import]>")
    parser.add_argument("targets",
                        help="run <sql_file[=target]>; remove <target>; " +
                             "copy <target>=<source>; mirror <target>=<source>; " +
                             "export <target>=<gs://...>; " +
                             "import <target>=<gs://.../table/*.json> or import <tables>=<gs://.../table_base_dir> --format=json; " +
                             "migrate <target>=<reference: schema.json|sql_file>. " +
                             "Table target is defined as [project.]dataset.table. Table name may contain wildcard, or date range, like tbl_2018*[0101-0818]. " +
                             "Multiple targets could be delimited by semicolon. " +
                             "If not set, project will be default to current GCP_PROJECT. ")
    parser.add_argument("-p", "--preview", help="preview list of targets only.", action="store_true")
    parser.add_argument("--append", help="append to existing table. ", action="store_true")
    parser.add_argument("--schema", help="schema file. ")
    parser.add_argument("--format", default="csv", help="csv, avro, json. default to csv.")
    parser.add_argument("--compression", help="gzip, deflate, snappy, default to none.")
    parser.add_argument("--gcs_staging", help="gcs staging bucket.")
    args = parser.parse_args()

    action_map = {"r": "run", "rm": "remove", "mr": "mirror", "mg": "migrate", "cp": "copy", "e": "export",
                  "i": "import", }
    action = action_map.get(args.action, args.action)

    for tgt in args.targets.split(";"):
        if action == "run":
            parts = tgt.split("=")
            tgt = DtTblRef(parts[1]) if len(parts) == 2 else None
            BQUtil().execute(parts[0], tgt, args.append, args.preview)
        elif action == "remove":
            BQUtil().delete(DtTblRef(tgt), args.preview)
        elif action == "copy":
            parts = tgt.split("=")
            BQUtil().copy(DtTblRef(parts[0]), DtTblRef(parts[1]), args.append, args.preview)
        elif action == "mirror":
            parts = tgt.split("=")
            BQUtil().mirror(DtTblRef(parts[0]), DtTblRef(parts[1]), args.preview)
        elif action == "migrate":
            parts = tgt.split("=")
            BQUtil().migrate(DtTblRef(parts[0]), parts[1], args.gcs_staging, args.preview)
        elif action == "export":
            parts = tgt.split("=")
            BQUtil().export(DtTblRef(parts[0]), parts[1], args.format, args.compression, args.preview)
        elif action == "import":
            parts = tgt.split("=")
            BQUtil().load(DtTblRef(parts[0]), parts[1], args.format, args.schema, args.append, args.preview)
