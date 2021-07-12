#!/usr/bin/env python
import json
import csv
import logging
from os import makedirs
from os import path
import random
import copy
import requests
import base64

# Reference:
#   experience: {"company":{ "name": "hallspot", "id": "hallspot",}, "start_date": "", "title": {}: "is_primary": true}
#   mapping: people(n) <--> (n)company
class ExperienceReader():
    DATA_DIR = path.join(path.dirname(path.realpath(__file__)), "_data")

    def __init__(self, data_dir = None):
        self._data = dict()
        self._path = dict()
        self._data_dir = data_dir if data_dir else ExperienceReader.DATA_DIR
        self._generated_dir = path.join(self._data_dir, "generated")
        if not path.exists(self._data_dir):
            makedirs(self._data_dir)
        if not path.exists(self._generated_dir):
            makedirs(self._generated_dir)

    def run(self):
        self._load_data()

    def _load_json(self, target):
        self._path[target] = path.join(self._data_dir, target + ".json")
        if path.isfile(self._path[target]):
            with open(self._path[target], "row") as json_file:
                self._data[target] = json.load(json_file)

    def _parse_company_data(self):
        # experience -> company list
        dtList = self._data["experience"]
        base_data = dtList[0]

        companies = {"Pear": 1, "Banana": 2, "Orange": 3}
        for pid in range(5):   # 5 people
            simulated_data = list()
            c_names = ["Pear", "Banana", "Orange"]
            random.shuffle(c_names)
            start_months = set()
            for company in c_names: # 3 jobs
                dt = copy.deepcopy(base_data)
                cid = companies[company]
                dt["company"]["name"] = company
                dt["company"]["id"] = company
                dt["company"]["linkedin_url"] = "linkedin.com/company/" + company
                dt["company"]["linkedin_id"] = 100 + cid
                dt["company"]["twitter_url"] = "twitter.com/" + company
                dt["company"]["website"] = company + ".garden"

                while True:
                    start_month = random.randint(1, 5)
                    if start_month in start_months:
                        continue
                    start_months.add(start_month)
                    break
                end_month = start_month + 1
                dt["start_date"] = "2020-0" + str(start_month)
                dt["end_date"] = "2020-0" + str(end_month)
                dt["is_primary"] = False

                simulated_data.append(dt)

            def start_date(x):
                return x["start_date"]

            # keep the last employment open-ended
            simulated_data.sort(key=start_date)
            simulated_data[2]["is_primary"] = True
            simulated_data[2]["end_date"] = None
            simulated_data_path = path.join(self._generated_dir, "e" + str(pid) + ".json.csv")
            self._write_data(simulated_data_path, pid, simulated_data)

    @staticmethod
    def _write_data(path, pid, data):
        with open(path, "w") as fout:
            for row in data:
                # str_line = json.dumps(row)
                # fout.write(str_line)
                # json.dump(row, fout)
                fout.write(str(pid))
                fout.write(",")
                fout.write(base64.b64encode(json.dumps(row).encode()).decode("utf-8"))
                fout.write("\n")


    def _load_data(self):
        self._load_json("experience")

        # build references
        self._parse_company_data()


if __name__ == "__main__":
    reader = ExperienceReader()
    reader.run()
