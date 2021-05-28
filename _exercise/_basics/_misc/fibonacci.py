def fibonacci(n: int):
    f = {0: 0, 1: 1}
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]
    return f[n]

def fibonacci3(n: int):
    "sum of three previous numbers"
    f = {0: 1, 1: 1, 2: 1}
    for i in range(3, n + 1):
        f[i] = f[i - 1] + f[i - 2] + f[i - 3]
    return f[n]


if __name__ == "__main__":
    # for n in [1, 2, 5, 50, 100]:
    #     print("{} => {}".format(n, fibonacci(n)))

    for n in range(0, 10):
        print("{} => {}".format(n, fibonacci3(n)))
