# solution maps the input matrix
def init_solution(matrix):
    return [[0 for col in row] for row in matrix]


def allowed(matrix, row, col, solution):
    if (row < 0 or row == len(matrix)) or (col < 0 or col ==  len(matrix)):   # beyond boundaries
        return False
    if not matrix[row][col]:    # blocked
        return False
    if solution[row][col]:      # visited?
        return False
    return True


def done(matrix, row, col, solution):
    if row == col == (len(matrix) - 1):
        for r in solution:
            print(" ".join([str(i) for i in r]))
        return True
    return False


def ProcessNode(matrix, row, col, solution):
    """
    Check if next node(s) allowed. If so, update the solution
    If it's end of the iteration (last node), print the solution
    """
    if done(matrix, row, col, solution):
        return

    # right, left, down, up
    for r, c in [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]:
        if allowed(matrix, r, c, solution):
            solution[r][c] = 1
            ProcessNode(matrix, r, c, solution)
            # rollback at parent node
            solution[r][c] = 0


if __name__ == "__main__":
    maze = [ [1, 0, 0, 0],
             [1, 1, 0, 1],
             [0, 1, 0, 0],
             [1, 1, 1, 1] ]

    ProcessNode(maze, 0, 0, init_solution(maze))