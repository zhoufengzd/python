
def check_dict_order():
    thisdict =	{
      "brand": "Ford",
      "model": "Mustang",
      "year": 1964
    }
    print(thisdict)

    thatdict =	{
      "model": "Mustang",
      "brand": "Ford",
      "year": 1964
    }
    print(thatdict)


def sort_dict():
    fruits = {"apple": 3, "peach": 2, "banana": 1}
    print(fruits)
    print("\nsort by key using sorted(): ")
    print(sorted(fruits.items(), key=lambda kv: kv[0]))
    print("\nsort by value using sorted() in reverse order: ")
    print(sorted(fruits.items(), key=lambda kv: kv[1], reverse=True))

    print("\niterate sorted keys")
    for k in sorted(fruits.keys()):
        print(f"{k}=>{fruits[k]}")


if __name__ == "__main__":
    # check_dict_order()
    sort_dict()
