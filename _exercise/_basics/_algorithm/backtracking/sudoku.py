# Sudoku vs tree: \
#    needs to traverse all cells to finishing placing one row or column
#    tree iteration likly only need to learn next node

def print_matrix(matrix):
    for row in matrix:
        print(" ".join([str(i) for i in row]))


def get_targets(matrix):
    """ return all empty cells """
    targets = list()
    for row in range(0, len(matrix)):
        for col in range(0, len(matrix)):
            if not matrix[row][col]:
                targets.append((row, col))
    return targets


def is_valid(matrix, current_row, current_col, n):
    row_size = col_size = len(matrix)
    # check if number used
    for col in range(col_size):
        if matrix[current_row][col] == n:
            return False

    for row in range(row_size):
        if matrix[row][current_col] == n:
            return False

    # mini square
    square_base_row = (current_row // 3) * 3
    square_base_col = (current_col // 3) * 3
    for row in range(3):
        for col in range(3):
            if matrix[square_base_row + row][square_base_col + col] == n:
                return False

    return True


def dfs(matrix, targets, tgt_idx, values):
    if tgt_idx == len(targets):
        print_matrix(matrix)
        print("--------------------")
        return

    row, col = targets[tgt_idx]
    for i in values:
        if is_valid(matrix, row, col, i):
            matrix[row][col] = i
            # dfs until done
            dfs(matrix, targets, tgt_idx + 1, values)
        # rollback
        matrix[row][col] = 0


if __name__ == "__main__":
    # for ms in [9]:  # matrix size
    #     mat = [[0 for col in range(ms)] for row in range(ms)]

    mat = [ [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

    v = [i for i in range(1, 9 + 1)]
    dfs(mat, get_targets(mat), 0, v)
