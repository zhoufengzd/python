import copy


def _is_completed(check_set) -> bool:
    for ct in check_set.values():
        if ct > 0:
            return False
    return True


def _trim_left(dt_list, check_set):
    i = 0
    while i < len(dt_list):
        c = dt_list[i]
        if c not in check_set:
            i += 1
            continue

        ct = check_set[c]
        if ct >= 0:
            break

        check_set[c] = ct + 1
        i += 1
    # print(f"i={i} {dt_list} => {dt_list[i:]}")
    return dt_list[i:]


def sliding_chars(dt_list, chars):
    result = list()

    n_size = len(dt_list)
    charset = dict()
    for c in chars:
        charset[c] = charset.get(c, 0) + 1

    result = list()
    check_set = copy.deepcopy(charset)
    tmp_list = list()
    for c in dt_list:
        if c not in check_set:
            if len(tmp_list):
                tmp_list.append(c)
            continue

        check_set[c] -= 1
        tmp_list.append(c)
        if _is_completed(check_set):
            tmp_list = _trim_left(tmp_list, check_set)
            if not result or len(result) > len(tmp_list):
                result = tmp_list.copy()
    return result


if __name__ == "__main__":
    for dt in ["ADOBECODEBANC"]:
        for cs in ["ABC", "AB", "AE", "AX"]:
            res = sliding_chars(dt, cs)
            print(f"{dt} =={cs}=> {res}")
