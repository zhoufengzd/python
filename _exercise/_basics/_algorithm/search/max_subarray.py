def max_subarray(numbers):
    """Find a contiguous subarray with the largest sum."""
    if not numbers:
        return (None, -1, -1)

    best_sum = current_sum = numbers[0]
    best_start = best_end = 0
    current_start = current_end = 0
    for idx, n in enumerate(numbers):
        current_end = idx
        if n > (current_sum + n):   # reset if previous do not add up
            current_start = current_end
            current_sum = n
        else:
            current_sum += n

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = current_end

    return (best_sum, best_start, best_end + 1) # the +1 is to make 'best_end' exclusive


if __name__ == "__main__":
    for dt in [[-11, 22, 33, -44], [-2, 1, -3, 4, -1, 2, 1, -5, 4], [-2, -1, 0, 1]]:
    # for dt in [[-11, 22, 33, -44]]:
        print(f"{dt} ? {max_subarray(dt)}")
