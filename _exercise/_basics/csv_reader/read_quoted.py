import csv

def read_quoted():
    with open("_data/quoted.csv") as fp:
        reader = csv.reader(fp, skipinitialspace=True)
        # reader = csv.reader(fp)
        for row in reader:
            print(row)


def read_quoted_dict_reader():
    import csv
    with open('_data/quoted.csv', 'r') as file:
        csv_file = csv.DictReader(file, skipinitialspace=True)
        for row in csv_file:    ##  {fieldname: value}
            print(row)


if __name__ == "__main__":
    # read_quoted()
    read_quoted_dict_reader()
