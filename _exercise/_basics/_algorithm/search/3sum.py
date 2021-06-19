
def iterate(numbers, sum):
    for i in range(len(numbers)):
        n = numbers[i]
        two_sum = sum - n
        visited = set()
        # if i == len(numbers), the loop will be skipped
        for j in range(i + 1, len(numbers)):
            m = numbers[j]
            if (two_sum - m) in visited:
                return (n, m, (two_sum - m))
            visited.add(m)

    return ()


if __name__ == "__main__":
    numbers = [1, 4, 45, 6, 10, 8]
    for dt in [22, 5, 13]:
        print(f"{dt} ? {iterate(numbers, dt)}")
