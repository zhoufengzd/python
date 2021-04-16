import csv

fields = ["Id", "Name", "Year"]
rows = [[1, "John L", 2019], [2, "Smith \"@\" T", 2019], [3, "Anita W", 2021]]

with open("id_year.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
