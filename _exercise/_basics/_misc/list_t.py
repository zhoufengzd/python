import copy

def sort_list(lst):
    s1 = copy.deepcopy(lst)
    s1.sort()
    print(f"sort(): {s1}")
    s2 = copy.deepcopy(lst)
    s2.sort(key=lambda e: e[1])
    print(f"sort(key=lambda e: e[1]): {s2}")
    s3 = copy.deepcopy(lst)
    s3.sort(reverse=True)
    print(f"sort(reverse=True): {s3}")


def reverse_list(lst):
    reversed = copy.deepcopy(lst)
    reversed.reverse()
    return reversed


def iterate_list(lst):
    for idx, e in enumerate(lst):
        print(f"l[{idx}] = {e}")


if __name__ == "__main__":
    l = [("A", 3), ("C", 1), ("B", 2)]
    iterate_list(l)
    sort_list(l)
