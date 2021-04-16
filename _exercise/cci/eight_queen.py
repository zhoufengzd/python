MATRIX_SIZE = 8

def place_queen(matrix, start_row, start_col):
    """"""
    if start_row == MATRIX_SIZE or start_col == MATRIX_SIZE:
        return matrix
    matrix[start_row][start_col] = 'q'
    return place_queen(matrix, start_row + 1, start_col)

def print_matrix(matrix):
    for i in range(MATRIX_SIZE):
        print(matrix[i])

if __name__ == "__main__":
    matrix = list()
    for i in range(MATRIX_SIZE):
        row = list()
        matrix.append(row)
        for j in range(MATRIX_SIZE):
            row.append('_')

    place_queen(matrix, 0, 0)
