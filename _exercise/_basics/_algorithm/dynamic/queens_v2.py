# N queens problem
def solveNQueens(n):
    output = []
    def dfs(row, queens, diags):
        if row == n:
            output.append(['.'*x + 'Q' + '.'*(n-x-1) for x in queens])
            return
        for col in range(n):
            if not any([row+col in diags, row-col-n-1 in diags, col in queens]):
                dfs(row + 1, queens + [col], diags | {row+col, row-col-n-1})
    dfs(0, [], set())
    return output


def print_matrix(matrix):
    for row in matrix:
        print(" ".join([f"{e}" for e in row]))


if __name__ == "__main__":
    for n in range(1, 10):
        print(f"n={n}")
        output = solveNQueens(n)
        for o in output:
            print_matrix(o)
            print("---------------")
