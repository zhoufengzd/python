# Sudoku vs tree: \
#    needs to traverse all cells to finishing placing one row or column
#    tree iteration likly only need to learn next node

def print_matrix(matrix):
    for row in matrix:
        print(" ".join([str(i) for i in row]))
    print("------------------")


def init_solution(matrix):
    # will use the same matrix for solution
    return matrix


def next_nodes(matrix, row, col):
    """"return next empty node if available"""
    row_size = col_size = len(matrix)
    while True:
        col += 1
        if col == col_size:
            col = 0
            row += 1
        if row == row_size:
            return []
        if not matrix[row][col]:
            return [(row, col)]


def allowed(matrix, row, col, n, solution):
    """check boundaries as well"""
    row_size = col_size = len(matrix)

    # check if number used
    for c in range(col_size):
        if matrix[row][c] == n:
            return False

    for r in range(row_size):
        if matrix[r][col] == n:
            return False

    # mini square
    square_base_row = (row // 3) * 3
    square_base_col = (col // 3) * 3
    for row in range(3):
        for col in range(3):
            if matrix[square_base_row + row][square_base_col + col] == n:
                return False

    return True


def done(matrix, row, col, solution):
    if row == col == (len(matrix) - 1):
        print_matrix(solution)
        return True
    return False


def process_node(matrix, row, col, n, solution):
    """
    Check if current node allowed. If so, update the solution
    If it's end of the iteration (last node), print the solution
    """
    if not allowed(matrix, row, col, n, solution):
        return
    solution[row][col] = n
    if done(matrix, row, col, solution):
        solution[row][col] = 0
        return

    for r, c in next_nodes(matrix, row, col):
        for n in range(1, 10):
            process_node(matrix, r, c, n, solution)

    # all child nodes are checked.
    solution[row][col] = 0


if __name__ == "__main__":
    m = [ [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

    for r, c in next_nodes(m, 0, -1):
        for n in range(1, 10):
            process_node(m, r, c, n, init_solution(m))
