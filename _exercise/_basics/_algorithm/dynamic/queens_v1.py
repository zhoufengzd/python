# Function to check if two queens threaten each other or not
def is_safe(matrix, row, col):
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
    while i >= 0 and j < N:
        if matrix[i][j] == 'Q':
            return False
        i = i - 1
        j = j + 1

    return True


def print_matrix(matrix):
    for row in matrix:
        print(" ".join([f"{e}" for e in row]))
    print()


def n_queen(matrix, row):

    # if `N` queens are placed successfully, print the solution
    if row == N:
        print_matrix(matrix)
        return

    # place queen at every square in the current row `row`
    # and recur for each valid movement
    for col in range(N):

        # if no two queens threaten each other
        if is_safe(matrix, row, col):
            # place queen on the current square
            matrix[row][col] = 'Q'

            # recur for the next row
            n_queen(matrix, row + 1)

            # backtrack and remove the queen from the current square
            matrix[row][col] = '–'


if __name__ == '__main__':
    # `N × N` chessboard
    N = 8
    # `matrix[][]` keeps track of the position of queens in
    # the current configuration
    mat = [['–' for x in range(N)] for y in range(N)]
    n_queen(mat, 0)