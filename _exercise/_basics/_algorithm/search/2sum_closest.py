def iterate(numbers, sum):
    import sys

    numbers.sort()
    low = 0
    high = len(numbers) - 1
    diff = sys.maxsize
    pair = ()
    while low < high:
        curr_sum = numbers[low] + numbers[high]
        if diff > abs(sum - curr_sum):
            diff = abs(sum - curr_sum)
            pair = (numbers[low], numbers[high])

        if curr_sum == sum:
            break
        elif curr_sum < sum:
            low += 1
        else:
            high -= 1

    return pair


if __name__ == "__main__":
    dt = [2, 7, 11, 15, 3]
    print(f"{dt}:")
    for tgt in [11, 9, 5]:
        print(f"-- {tgt} ? {iterate(dt, tgt)}")
