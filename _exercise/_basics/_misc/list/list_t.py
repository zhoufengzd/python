import copy

def sort_list():
    l = [[2, 30], [1, 40]]
    s1 = copy.deepcopy(l)
    s1.sort()
    s2 = copy.deepcopy(l)
    s2.sort(key=lambda e: e[1])
    s3 = copy.deepcopy(l)
    s3.sort(reverse=True)
    print(f"{l} => sort: {s1} | sort by e[1]: {s2} | reverse=True: {s3}")

def reverse_list(l):
    reversed = copy.deepcopy(l)

    reversed.reverse()
    return reversed

def iterate_list(l):
    for idx, e in enumerate(l):
        print(f"l[{idx}] = {e}")

if __name__ == "__main__":
    # sort_list()

    systems = ['Windows', 'macOS', 'Linux']
    print("{} => {}".format(systems, reverse_list(systems)))

    iterate_list(systems)
