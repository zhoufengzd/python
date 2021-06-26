
def iterate(numbers, sum):
    visited = set()
    for i in numbers:
        if (sum - i) in visited:
            return (i, (sum - i))
        visited.add(i)
    return ()


def max_subarray(numbers):
    """Find the largest sum of any contiguous subarray."""
    best_sum = 0
    current_sum = 0
    for x in numbers:
        current_sum = max(0, current_sum + x)
        best_sum = max(best_sum, current_sum)
    return best_sum


def findMaxZeroCount(arr):
    orig_zero_count = 0

    max_diff = 0
    curr_max = 0
    for i in arr:

        # Count of zeros in original
        # array (Not related to
        # Kadane's algorithm)
        if i == 0:
            orig_zero_count += 1

        # Value to be considered for
        # finding maximum sum
        val = 1 if i == 1 else -1

        # Update current max and max_diff
        curr_max = max(val, curr_max + val)
        max_diff = max(max_diff, curr_max)

    max_diff = max(0, max_diff)

    return orig_zero_count + max_diff


if __name__ == "__main__":
    for dt in [[ 0, 1, 0, 0, 1, 1, 0 ]]:
        print(f"{dt} ? {findMaxZeroCount(dt)}")
