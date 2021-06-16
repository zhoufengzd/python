import itertools


def subsets_n(dt_set, subset_size):
    res = list()
    for e in itertools.combinations(dt_set, subset_size):
        if e not in res:
            res.append(e)
    return res


def subsets(dt_set):
    result = list()
    for n in range(len(dt_set)):
        result.append(subsets_n(dt_set, n))
    return result


if __name__ == "__main__":
    for l in [[1, 2, 3], [1, 1, 2]]:
        print("{} => {}".format(l, subsets(l)))
