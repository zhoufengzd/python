def iterate(arr1, arr2, sum):
    import sys

    arr1.sort()
    arr2.sort()
    idx1 = 0
    idx2 = len(arr2) - 1
    diff = sys.maxsize
    pair = ()
    while idx1 < len(arr1) and idx2 >=0 :
        curr_sum = arr1[idx1] + arr2[idx2]
        if diff > abs(sum - curr_sum):
            diff = abs(sum - curr_sum)
            pair = (arr1[idx1], arr2[idx2])

        if curr_sum == sum:
            break
        elif curr_sum < sum:
            idx1 += 1
        else:
            idx2 -= 1

    return pair


if __name__ == "__main__":
    dt1 = [1, 4, 5, 7]
    dt2 = [10, 20, 30, 40]
    print(f"{dt1}, {dt2}:")
    for tgt in [38, 11, 9, 5]:
        print(f"-- {tgt} ? {iterate(dt1, dt2, tgt)}")
