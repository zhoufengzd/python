# merge / sorted list

def merge_schedule(schedules):
    if not schedules:
        return schedules

    schedules.sort()
    merged = list()
    for idx, curr_block in enumerate(schedules):
        if idx == 0:
            base_block = curr_block
            continue

        # overlap => [base_block.start, max(base_block.end, curr_block.end)]
        if base_block[1] >= curr_block[0]:
            base_block = [base_block[0], curr_block[1] if curr_block[1] > base_block[1] else base_block[1]]
            continue

        # no overlap
        merged.append(base_block)
        base_block = curr_block

    merged.append(base_block)
    return merged


if __name__ == "__main__":
    for s in [[[]], [[1, 2]], [[1, 3], [2, 4]], [[1, 2], [3, 4]], [[1, 4], [2, 3], [3, 5]], [[2, 3], [1, 4], [3, 5]]]:
        print("{} => {}".format(s, merge_schedule(s)))
