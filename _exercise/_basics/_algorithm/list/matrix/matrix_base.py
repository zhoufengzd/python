# matrix
#   2D matrix = [[row#1], [row#2],...]
#   Variations / challenges is on the iteration

class Matrix:
    def __init__(self, row_size, col_size):
        self.matrix = list()
        self.row_size = row_size
        self.col_size = col_size
        n = 1
        for i in range(row_size):
            self.matrix.append([i for i in range(n, n + col_size)])
            n += col_size

    def __str__(self):
        for row in self.matrix:
            print(" ".join([f"{e:2}" for e in row]))


if __name__ == "__main__":
    mx = Matrix(4, 4)
    print(mx)
