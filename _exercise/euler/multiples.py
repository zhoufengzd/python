# sum all multiples of input numbers

def _sum_n_multiples(n, max_n):
    """sum of multiples of n under max_n, 1 * n + 2 * n + ... m * n"""
    m = (max_n - 1) // n
    return int((m * (m + 1) / 2) * n)


if __name__ == "__main__":
    for max_number in [10, 100, 1000]:
        sum = 0
        for numbers in [[3, 5]]:
            for n in numbers:
                sum += _sum_n_multiples(n, max_number)
        print(f"sum of multiples of {numbers} under {max_number} = {sum}")
