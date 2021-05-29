#

def iterate_dict(dt):
    print("\n-- iterate by unsorted key: ")
    for k in dt:
        print(f"dt[{k}] => {dt[k]}")

    print("\n -- iterate by unsorted key, value: ")
    for k, v in dt.items():
        print(f"{k} => {v}")

def check_dict(dt):
    print("## -- by default dictionary is not sorted: ")
    print(dt)


def sort_dict(dt):
    print("\n -- sorted by key using sorted(): ")
    print(sorted(dt.items(), key=lambda kv: kv[0]))
    print("\n -- sorted by value using sorted() in reverse order: ")
    print(sorted(dt.items(), key=lambda kv: kv[1], reverse=True))

    print("\n -- iterate sorted keys")
    for k in sorted(dt.keys()):
        print(f"{k}=>{dt[k]}")


if __name__ == "__main__":
    fruits = {"apple": 3, "peach": 2, "banana": 1}

    check_dict(fruits)
    iterate_dict(fruits)
    sort_dict(fruits)
