
def print_matrix(matrix):
    for row in matrix:
        print(" ".join([str(i) for i in row]))
    print("------------------")


def init_solution(matrix):
    # solution maps the input matrix
    return [[0 for col in row] for row in matrix]


def next_nodes(matrix, row, col):
    # child nodes: right, left, down, up
    return [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]


def allowed(matrix, row, col, solution):
    if (row < 0 or row == len(matrix)) or (col < 0 or col ==  len(matrix)):   # beyond boundaries
        return False
    if not matrix[row][col]:    # blocked
        return False
    if solution[row][col]:      # visited?
        return False
    return True


def done(matrix, row, col, solution):
    if row == col == (len(matrix) - 1) or matrix[row][col] == 9:
        print_matrix(solution)
        return True
    return False


def process_node(matrix, row, col, solution):
    """
    Check if next node(s) allowed. If so, update the solution
    If it's end of the iteration (last node), print the solution
    """
    if not allowed(matrix, row, col, solution):
        return
    solution[row][col] = 1
    if done(matrix, row, col, solution):
        solution[row][col] = 0
        return

    for r, c in next_nodes(matrix, row, col):
        process_node(matrix, r, c, solution)

    # all child nodes are checked.
    solution[row][col] = 0


if __name__ == "__main__":
    maze1 = [   [1, 0, 0, 0],
                [1, 1, 0, 1],
                [0, 1, 0, 0],
                [1, 1, 1, 1] ]
    maze2 = [   [1, 0, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 9, 0, 1, 1],
                [1, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1] ]
    for mz in [maze1, maze2]:
        process_node(mz, 0, 0, init_solution(mz))