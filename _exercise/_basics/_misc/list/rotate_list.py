# matrix operation

# adjust positions if out of bound
from typing import List


def __adjust_pos(pos, length):
    """
    move out of bounds pos to the start or end of the array
    expect pos < length
    """
    if pos < 0:
        # shift left:  1 2 0 <= 0 1 2, here pos -1 => pos 2 = -1 + 3 (length of array)
        return pos + length
    elif pos >= length:
        #  shift right: 0 1 2 => 2 0 1, here pos 3 => pos 0 = 3 - 3 (length of array)
        return pos - length
    return pos


# rotate
def rotate(lst, n_pos):
    """rotate a list by +/- n positions"""
    l_length = len(lst)
    n_pos = n_pos % l_length
    if not n_pos:
        return lst

    rotated = [None] * l_length
    for idx, e in enumerate(lst):
        rotated[__adjust_pos(idx + n_pos, l_length)] = e

    return rotated


# array to matrix
def __to_matrix(lst, column_size):
    """
                                | 1 2 3 |
    [1, 2, 3, 4, 5, 6, 7, 8] => | 8   4 |
                                | 7 6 5 |
    """
    l_length = len(lst)
    if not column_size or column_size >= l_length:
        return [lst]

    if column_size == 1:
        row_size = l_length
    elif l_length // column_size == 1:
        row_size = 2
    else:  # top row + bottom row + side columns in between
        row_size = ((l_length - 2 * column_size + 1) // 2 + 2)
    matrix = [[" "] * column_size for j in range(row_size)]

    current_row = 0
    current_col = 0
    direction = "right"  # "right", "down", "left", "up"
    for e in lst:
        # top row
        if direction == "right":
            if current_col <= column_size - 1:
                matrix[current_row][current_col] = e
                current_col += 1
            if current_col >= column_size:
                current_col = column_size - 1
                current_row += 1
                direction = "down" if row_size > 2 else "left"
            continue
        # right column
        elif direction == "down":
            if current_row < row_size - 1:
                matrix[current_row][current_col] = e
                current_row += 1
            if current_row >= row_size - 1:
                current_row = row_size - 1
                direction = "left"
            continue
        # bottom row
        elif direction == "left":
            if current_col >= 0:
                matrix[current_row][current_col] = e
                current_col -= 1
            if current_col < 0:
                current_col = 0
                current_row = row_size - 2
                direction = "up"
            continue
        # left column
        elif direction == "up":
            if current_row >= 1:
                matrix[current_row][current_col] = e
                current_row -= 1
            if current_row == 0:
                break
    return matrix


def __print_matrix(matrix):
    for row in matrix:
        print(" | ".join([f"{e:2}" for e in row]))


def __test_array_rotation_v1():
    for lst in [[0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]:
        for npos in range(-5, 5):
            r = rotate(lst, npos)
            print(f"rotate {npos}: {lst} => {r}")


def __test_array_rotation_v2():
    for lst in [[0, 1]]:
        for n_pos in [10, 11]:
            r = rotate(lst, n_pos)
            print(f"rotate {n_pos}: {lst} => {r}")


def __test_array_to_matrix():
    lst: List[int] = [e for e in range(1, 9)]
    print(f"input array: {lst}")
    for c_size in range(10):
        print(f"column size = {c_size}")
        __print_matrix(__to_matrix(lst, c_size))


if __name__ == "__main__":
    dt = [e for e in range(1, 13)]
    col_size = 4
    m = __to_matrix(dt, col_size)
    print("-- input matrix: ")
    __print_matrix(m)

    rotated_matrix = __to_matrix(rotate(dt, 18), col_size)
    print("-- rotated: ")
    __print_matrix(rotated_matrix)
