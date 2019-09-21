from google.cloud import bigquery
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.job import QueryJobConfig
from google.cloud.bigquery.table import TableReference


class TableReferenceBuilder():
    """ Take free format table name in [project.dataset.table | dataset.table | table] and build table reference """

    def __init__(self, table_name, dataset_name=None, project_name=None):
        self._project = project_name
        self._dataset = dataset_name
        self._table = table_name

        parts = table_name.replace(":", ".").split(".")
        if len(parts) == 3:  # project.dataset.table
            self._project = parts[0]
            self._dataset = parts[1]
            self._table = parts[2]
        elif len(parts) == 2:  # dataset.table
            self._dataset = parts[0]
            self._table = parts[1]

        self._dataset_ref = DatasetReference(dataset_id=self._dataset, project=self._project)
        self._table_ref = TableReference(dataset_ref=self._dataset_ref, table_id=self._table)

    @property
    def table_reference(self):
        return self._table_ref

    @property
    def table(self):
        return self._table

    @property
    def dataset_reference(self):
        return self._dataset_ref

    @property
    def dataset(self):
        return self._dataset

    @property
    def project(self):
        return self._project


class BigQueryRunner:
    def __init__(self, project, dataset=None, quiet=False):
        self._project = project
        self._dataset = dataset
        self._quiet = quiet
        self._query_job = None

    def execute(self, query, destination_table, write_disposition="WRITE_TRUNCATE", allow_large_results=True):
        """
        :param query_file: query file path
        :param destination_table: target table
        :param write_disposition:  default is to replace existing table. To append: WRITE_APPEND
        :param allow_large_results: default to True
        :return:
        """
        query_configuration = QueryJobConfig()
        query_configuration.use_legacy_sql = False
        if destination_table:
            ref = TableReferenceBuilder(destination_table, self._dataset, self._project)
            query_configuration.write_disposition = write_disposition
            query_configuration.default_dataset = ref.dataset_reference
            query_configuration.destination = ref.table_reference
            query_configuration.allow_large_results = allow_large_results

        sql_query = self.__get_query(query)
        if not self._quiet:
            print ("-- #### {}\n{}\n".format(destination_table or "", sql_query))

        self._query_job = bigquery.Client(project=self._project).query(sql_query, job_config=query_configuration)
        if self._query_job.errors:
            raise Exception(self._query_job.errors)

    def fetch(self, query, timeout_seconds=30):
        self._query_job = bigquery.Client(project=self._project).query(self.__get_query(query))
        if self._query_job.done:
            return self._query_job.result(timeout=timeout_seconds)
        return None

    def fetch_one(self, query, timeout_seconds=30):
        self._query_job = bigquery.Client(project=self._project).query(self.__get_query(query))
        if self._query_job.done:
            rows = self._query_job.result(timeout=timeout_seconds)
            for row in rows:
                return row
        return None

    def __get_query(self, query):
        import os.path
        if not os.path.exists(query):
            return query
        with open(query, 'r') as f:
            return f.read()

    @property
    def done(self):
        return self._query_job.done()
