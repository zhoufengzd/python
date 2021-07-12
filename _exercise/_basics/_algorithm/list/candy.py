# There are matrix_size children standing in a line with some rating value. You want to distribute a minimum number of candies to these children such that:
# Each child must have at least one candy.
# The children with higher ratings will have more candies than their neighbours.

def iterate(numbers):
    res = [1 for i in numbers]

    # check left
    for idx in range(1, len(numbers)):
        if numbers[idx] > numbers[idx-1]:
            res[idx] = res[idx-1] + 1

    # check right, but maintain previous peak
    for idx in range(len(numbers) - 2, -1, -1):
        if numbers[idx] > numbers[idx+1]:
            res[idx] = max(res[idx], res[idx+1] + 1)

    return res


if __name__ == "__main__":
    for dt in [[1, 5, 2, 1], [3, 2, 3, 2, 1], [1, 2, 3, 1], [1, 3, 2, 1], [2, 1, 5]]:
        print(f"{dt} => {iterate(dt)}")
