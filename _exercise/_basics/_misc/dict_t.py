#
def int_dict_v1(keys):
    return dict.fromkeys(keys)


def int_dict_v2(keys):
    return {k: None for k in keys}


def iterate_dict(dt):
    print("\n-- iterate by unsorted key: ")
    for k in dt:
        print(f"dt[{k}] => {dt[k]}")

    print("\n -- iterate by unsorted key, value: ")
    for k, v in dt.items():
        print(f"{k} => {v}")


def iterate_dict_key_sorted(dt):
    print("\n -- iterate sorted keys")
    for k in sorted(dt.keys()):
        print(f"{k}=>{dt[k]}")


def check_dict(dt):
    print("## -- by default dictionary is not sorted: ")
    print(dt)


def sort_dict(dt):
    print("\n -- sorted by key: ")
    print(sorted(dt.items(), key=lambda kv: kv[0]))
    print("\n -- sorted by key in reverse order: ")
    print(sorted(dt.items(), key=lambda kv: kv[0], reverse=True))
    print("\n -- sorted by value: ")
    print(sorted(dt.items(), key=lambda kv: kv[1]))


if __name__ == "__main__":
    # fruits = int_dict_v1([2, 3, 1])
    fruits = int_dict_v2([2, 3, 1])
    fruits[1] = "Banana"
    fruits[2] = "Apple"
    fruits[3] = "Cranberry"

    check_dict(fruits)
    iterate_dict(fruits)
    iterate_dict_key_sorted(fruits)
    sort_dict(fruits)
