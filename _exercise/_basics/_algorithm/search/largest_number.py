
def iterate(numbers):
    max_length = len(str(max(numbers)))
    def padding(n):
        n_str = str(n)
        pad = n_str[0]
        return n_str.ljust(max_length, pad)

    numbers.sort(key=lambda e: padding(e), reverse=True)
    return "".join([str(i) for i in numbers])


if __name__ == "__main__":
    for dt in [[3, 30, 34, 5, 9], [1, 34, 3, 98, 9, 76, 44, 4]]:
        print(f"{dt} ? {iterate(dt)}")
