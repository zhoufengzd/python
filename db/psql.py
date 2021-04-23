#!/usr/bin/env python

import argparse
import csv
import datetime
import os
import os.path
import os.path
from contextlib import contextmanager

import psycopg2.pool
# from dotenv import load_dotenv


class DBConnection(object):
    # default constants
    DEFAULT_MIN_POOL = 1
    DEFAULT_MAX_POOL = 10

    def __init__(self, profile=None):
        self.driver = None
        # if os.path.exists(profile):
        #     load_dotenv(profile)

    def connect(self, db_name, db_host=None, db_user=None, db_pwd=None, db_port=None, min_pool=None, max_pool=None):
        if not db_host:
            db_host = os.getenv("POSTGRES_HOST", "127.0.0.1")
        if not db_port:
            db_port = int(os.getenv("POSTGRES_PORT", "5432"))
        if not db_name:
            db_name = os.getenv("POSTGRES_DATABASE", "postgres")
        if not db_user:
            db_user = os.getenv("POSTGRES_USER", os.getlogin())
        if not db_pwd:
            db_pwd = os.getenv("POSTGRES_PASSWORD", os.getenv("PGPASSWORD", ""))
        if not min_pool:
            min_pool = DBConnection.DEFAULT_MIN_POOL
        if not max_pool:
            max_pool = DBConnection.DEFAULT_MAX_POOL
        self.driver = psycopg2.pool.ThreadedConnectionPool(min_pool, max_pool, host=db_host, port=db_port,
                                                           database=db_name, user=db_user, password=db_pwd)

    @contextmanager
    def get_cursor(self, autocommit):
        con = self.driver.getconn()
        if autocommit:
            con.autocommit = True
        try:
            yield con.cursor()
        finally:
            self.driver.putconn(con)


class DBClient(DBConnection):
    # sql & command format
    SQL_TRUNCATE_TABLE_FMT = "TRUNCATE TABLE %s"
    SQL_INSERT_FMT = "INSERT INTO %s (%s) VALUES (%s)"
    SQL_SELECT_FMT = "SELECT * FROM {};"

    CMD_IMPORT_FMT = "COPY %s%s FROM STDIN WITH DELIMITER \'%s\' CSV %s"
    CMD_EXPORT_FMT = "COPY (%s) TO \'%s\' WITH HEADER CSV DELIMITER ','"

    # filename
    DATE_TIME_FMT = "%Y%m%d_%H%M%S"

    def __init__(self, profile=None):
        self.__reset_table_info()

    def run_sql(self, sql, sql_args=None, autocommit=True):
        query, is_sql_file = self.__get_query(sql)
        with self.get_cursor(autocommit) as cursor:
            if sql_args:
                cursor.execute(str(cursor.mogrify(query, sql_args)))
            else:
                cursor.execute(query)

    def fetch(self, sql, sql_args=None, autocommit=True, row_count=0):
        with self.get_cursor(autocommit) as cursor:
            cursor.execute(cursor.mogrify(sql, sql_args))
            if row_count > 0:
                return cursor.fetchmany(size=row_count), cursor.description
            return cursor.fetchall(), cursor.description

    # load table from csv file. will automatically map columns if header row is defined
    def load_csv(self, table_name, csv_file, truncate_table=False, has_header=False, csv_delimiter=","):
        self.__reset_table_info()
        self.table = table_name

        if truncate_table:
            self.truncate_table(self.table)

        column_opt = ""
        header_opt = ""
        if has_header:
            self.__read_header_row(csv_file, csv_delimiter)
            header_opt = "HEADER"
            column_opt = "(" + ",".join(self.columns) + ")"
            self.__build_insert_sql()
        copy_cmd = DBClient.CMD_IMPORT_FMT % (self.table, column_opt, csv_delimiter, header_opt)
        # print(copy_cmd)
        with open(csv_file, 'r') as in_file:
            with self.get_cursor(True) as cursor:
                cursor.copy_expert(copy_cmd, in_file)

    def load_row(self, table_name, row_data, column_names=None):
        if (self.table != table_name) or (column_names is not None and self.columns != column_names):
            self.__reset_table_info()
            self.table = table_name
            self.columns = column_names
            self.__build_insert_sql()
        self.run_sql(self.insert_sql, row_data)

    def truncate_table(self, table_name):
        self.run_sql(DBClient.SQL_TRUNCATE_TABLE_FMT % table_name)

    def export_csv(self, export_target, csv_file=None, with_header=False, csv_delimiter=","):
        query, is_sql_file = self.__get_query(export_target)
        if is_sql_file:  # query sql file
            if csv_file is None:
                csv_file = export_target + ".out.csv"
        else:
            if export_target.upper().startswith("SELECT "):  # live query
                if csv_file is None:
                    csv_file = datetime.datetime.now().strftime(DBClient.DATE_TIME_FMT) + ".out.csv"
            else:  # table name
                query = DBClient.SQL_SELECT_FMT.format(export_target)
                if csv_file is None:
                    csv_file = export_target + ".out.csv"

        rows, headers = self.fetch(query)
        with open(csv_file, 'w') as of:
            if with_header:
                for (idx, col_meta) in enumerate(headers):
                    if idx > 0:
                        of.write(",")
                    of.write("\"" + col_meta[0] + "\"")
                of.write('\n')

            for row in rows:
                for (idx, col_value) in enumerate(row):
                    if idx > 0:
                        of.write(",")
                    if not col_value:
                        continue

                    if type(col_value) is str:
                        of.write("\"" + col_value.replace('"', '""') + "\"")
                    else:
                        of.write(str(col_value))
                of.write('\n')

    def __get_query(self, raw_query):
        is_sql_file = False
        query = raw_query
        if os.path.isfile(raw_query):
            is_sql_file = True
            with open(raw_query, 'r') as in_file:  # sql file
                query = in_file.read()
        if not query.endswith(";"):
            query = query + ";"
        return query, is_sql_file

    def __reset_table_info(self):
        self.table = None
        self.columns = None
        self.insert_sql = None

    def __read_header_row(self, csv_file, csv_delimiter, csv_quotechar="\""):
        with open(csv_file, 'r') as in_file:
            row_reader = csv.reader(in_file, delimiter=csv_delimiter, quotechar=csv_quotechar)
            self.columns = next(row_reader)  # gets the first line

    def __build_insert_sql(self):
        value_fmt = ""
        i = 0
        while i < len(self.columns):
            if i > 0:
                value_fmt += ", "
            value_fmt += "%s"
            i += 1

        self.insert_sql = DBClient.SQL_INSERT_FMT % (self.table, ",".join(self.columns), value_fmt)
        # print(self.insert_sql)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="action, including: <[r|run_sql] | [i|import] | <[e|export]>")
    parser.add_argument("targets",
                        help="action targets. Sql, sql file, or table. multiple targets could be delimited by semicolon.  To run sql: <[sql |sql file]>.  To import or export: <[sql |sql file |table]> [= <csv.file:[no_header |truncate]>] ")
    parser.add_argument("--profile",
                        help="postgres environment profile that include \$POSTGRES_HOST and other settings.")
    parser.add_argument("--host", help="db_host. default to \$POSTGRES_HOST, then localhost.")
    parser.add_argument("-u", "--user", help="db_user. default to \$POSTGRES_USER, then current login.")
    parser.add_argument("--password", help="password. default to \$POSTGRES_PASSWORD, then \$PGPASSWORD.")
    parser.add_argument("-d", "--database", help="database name. default to \$POSTGRES_DATABASE, then postgres.")
    parser.add_argument("-p", "--port", help="host_port. default to \$POSTGRES_PORT, then 5432.")
    args = parser.parse_args()

    action = "run_sql"
    if args.action.startswith("e"):
        action = "export"
    elif args.action.startswith("i"):
        action = "import"

    dbclient = DBClient(args.profile)
    dbclient.connect(args.database, args.host, args.user, args.password, args.port)
    for tgt in args.targets.split(";"):
        # simple query
        if action == "run_sql":
            dbclient.run_sql(tgt)
            continue

        # import and export are table based actions
        table_name = tgt
        csv_file = None
        truncate_table = False
        with_header = True

        options = tgt.split("=")
        if len(options) > 1:
            table_name = options[0]
            csv_options = options[1].split(":")
            csv_file = csv_options[0]
            truncate_table = "truncate" in csv_options
            if "no_header" in csv_options:
                with_header = False

        if action == "import":
            dbclient.load_csv(table_name, csv_file, truncate_table, with_header)
        else:
            dbclient.export_csv(table_name, csv_file, with_header)
