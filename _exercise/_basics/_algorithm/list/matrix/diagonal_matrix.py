"""
Print the elements of a m x n matrix diagonally.

eg.,

Given

1 2 3 4
5 6 7 8
9 a b c

1 2 3 4 m
5 6 7 8 n
9 a b c q
r s t w y

print

1
2 5
3 6 9
4 7 a
8 b
c

"""

def init_matrix(row_size, col_size):
    matrix = list()
    n = 1
    for i in range(row_size):
        l = list()
        for j in range(row_size):
            l.append(n)
            n += 1
        matrix.append(l)
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(" ".join([f"{e:2}" for e in row]))


def get_diagonal_elements(matrix, row_size, col_size, row_id, col_id):
    row_output = list()
    row_output.append(matrix[row_id][col_id])
    current_row_id = row_id
    current_col_id = col_id
    while True:
        row_next = current_row_id + 1
        col_next = current_col_id - 1
        if row_next >= row_size or col_next < 0:
            break
        row_output.append(matrix[row_next][col_next])
        current_row_id = row_next
        current_col_id = col_next
    return row_output


def to_diagonally(matrix):
    converted = list()

    row_size = len(matrix)
    col_size = len(matrix[0])
    row_id = 0
    while True:
        if row_id >= row_size:
            break

        current_row = matrix[row_id]
        if row_id == 0: # the first row needs to iterate every element
            for col_id, i in enumerate(current_row):
                converted.append(get_diagonal_elements(matrix, row_size, col_size, row_id, col_id))
        else: # following rows only need to iterate the last element
            converted.append(get_diagonal_elements(matrix, row_size, col_size, row_id, col_size - 1))
        row_id += 1
    return converted


if __name__ == "__main__":
    mx = init_matrix(4, 4)
    print_matrix(mx)

    print("-------------")
    mc = to_diagonally(mx)  # converted
    print_matrix(mc)
