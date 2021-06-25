def iterate(numbers):
    expected = set([e for e in range(1, len(numbers) + 1)])
    for i in numbers:
        if i in expected:
            expected.remove(i)
    return next(iter(expected)) if expected else None


if __name__ == "__main__":
    for dt in [[1, 2, 0], [1], [3, 4, -1, 1], [7, 8, 9, 11, 12, 1]]:
        print(f"{dt} ? {iterate(dt)}")
