# example of csv reader
# -- https://www.programiz.com/python-programming/reading-csv-files

def pd_read_csv():
    import pandas as pd
    dt = pd.read_csv("_data/id_year.csv")

def read_csv():
    import csv
    with open('_data/id_year.csv', 'row') as file:
        # additional option:
        #   skipinitialspace=True, delimiter = '\t', quoting=csv.QUOTE_NONNUMERIC
        reader = csv.reader(file)
        for row in reader: ## return list of data
            print(row)


def read_csv_dict():
    import csv
    with open('_data/id_year.csv', 'row') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:    ##  {fieldname: value}
            # print(type(row))
            print(row)


def sniff_csv():
    import csv
    with open('_data/id_year.csv', 'row') as csvfile:
        sample = csvfile.read(64)
        has_header = csv.Sniffer().has_header(sample)
        print(has_header)
        deduced_dialect = csv.Sniffer().sniff(sample)

def read_csv_url():
    import csv, urllib.request

    url = 'http://winterolympicsmedals.com/medals.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    for row in cr:
        print(row)


def read_csv_user():
    import csv
    user_map = dict()
    with open('user_lists.csv', 'row') as file:
         # CSV files and create User instances from the data:
         #  (a) user_lists.csv: each line in the csv file represents a user. The line
         #      number (indexed by 0) is the user_id, and the values in each line
         #      represent this user's favorite things.
        reader = csv.reader(file)
        uid = 0
        for row in reader:
            favorites = [ e.strip() for e in row]
            # print(f"{uid}: {favorites}")
            user_map[uid] = favorites
            uid += 1
        print(user_map)


def read_followed():
    import csv
    follow_map = dict()
    with open('followed_users.csv', 'row') as file:
      # (b) followed_users.csv: each line in the csv includes two user ids, indicating
      #     that the first user_id follows the second user_id. For example, a line with
      #     `2 0` indicates that User 2 follows User 0.
        reader = csv.reader(file, delimiter = ' ')
        for row in reader:
            if not row or len(row) < 2:
                continue

            uid = row[0]
            followed = follow_map.get(uid, None)
            if not followed:
                followed = set()
                follow_map[uid] = followed
            followed.add(row[1])
        print(follow_map)

if __name__ == "__main__":
    # read_csv()
    # read_csv_dict()
    # sniff_csv()
    # read_csv_url()
    read_csv_user()
    # read_followed()
