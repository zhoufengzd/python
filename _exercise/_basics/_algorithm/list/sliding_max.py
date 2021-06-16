def sliding_max(dt_list, k):
    result = list()

    n_size = len(dt_list)
    for i in range(0, n_size):
        if i + k > n_size:
            break

        win_max = dt_list[i]
        for j in range(i + 1, i + k):
            if dt_list[j] > win_max:
                win_max = dt_list[j]
        result.append(win_max)
    return result


if __name__ == "__main__":
    for dt in [[1, 3, -1, -3, 5, 3, 6, 7], [1, 3, 2, 4, 1], [2, 1]]:
        for ws in [3]:
            dt_max = sliding_max(dt, ws)
            print(f"{dt} => {dt_max}")
