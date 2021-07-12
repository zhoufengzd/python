# Function to check if two queens threaten each other or not
def is_safe(matrix, row, col, matrix_size):
    # return false if two queens share the same column
    for i in range(row):
        if matrix[i][col] == 'Q':
            return False

    # return false if two queens share the same `` diagonal
    (i, j) = (row, col)
    while i >= 0 and j >= 0:
        if matrix[i][j] == 'Q':
            return False
        i = i - 1
        j = j - 1

    # return false if two queens share the same `/` diagonal
    (i, j) = (row, col)
    while i >= 0 and j < matrix_size:
        if matrix[i][j] == 'Q':
            return False
        i = i - 1
        j = j + 1

    return True


def print_matrix(matrix):
    for row in matrix:
        print(" ".join([f"{e}" for e in row]))
    print()


def n_queen(matrix, row, matrix_size):
    # stop check
    if row == matrix_size:
        print_matrix(matrix)
        return

    # place queen at every square in the current row `row`
    # and recur for each valid movement
    for col in range(matrix_size):

        # if no two queens threaten each other
        if is_safe(matrix, row, col, matrix_size):
            # place queen on the current square
            matrix[row][col] = 'Q'

            # recur for the next row
            n_queen(matrix, row + 1, matrix_size)

            # backtrack and remove the queen from the current square
            matrix[row][col] = '–'


if __name__ == '__main__':
    for ms in [8]:  # ms: matrix size
        mat = [['–' for col in range(ms)] for row in range(ms)]
        n_queen(mat, 0, ms)
