
def iterate(numbers, sum):
    visited = set()
    for i in numbers:
        if (sum - i) in visited:
            return (i, (sum - i))
        visited.add(i)
    return ()


if __name__ == "__main__":
    numbers = [2,7,11,15, 3]
    for dt in [11, 9, 5]:
        print(f"{dt} ? {iterate(numbers, dt)}")
