# Given an array that contains both positive and negative integers,
#   find the product of the maximum product subarray.
# Expected Time complexity is O(n) and only O(1) extra space can be used.
# https://www.techiedelight.com/find-maximum-product-subarray-given-array/

def max_products(numbers):
    if not numbers:
        return None
    if len(numbers) == 1:
        return numbers[0]

    # maintain current maximum and minimum product
    #   curr_max >= 0, and curr_min <= 0
    curr_max = curr_min = max_prod = 0

    for i in numbers:
        prv_max = curr_max
        prv_min = curr_min

        # update the current min / max while i is included
        # if i = 0, then curr_max = curr_min = 0
        # if i <= 0, curr_max = i * prv_min, curr_min = min(i, i * prv_max)
        curr_max = max(i, i * prv_max, i * prv_min)
        curr_min = min(i, i * prv_max, i * prv_min)
        print(f"i={i}: {prv_max}=>{curr_max}, {prv_min}=>{curr_min}")
        max_prod = max(max_prod, curr_max)
    return max_prod


if __name__ == "__main__":
    # for dt in [[-1, -2, -3, -4, -5], [6, -3, -10, 0, 2, 100], [-6, 4, -5, 8, -10, 0, 8]]:
    for dt in [[-1], [1], [-1, 1, 2, 3, -4, 5], [1, 2, 3], [-1, 2, -3, 1, -2, 1, -3], [-2, 3, 4, 5, 0, -6]]:
        print(f"{dt} => {max_products(dt)}\n")
