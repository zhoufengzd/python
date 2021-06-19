"""
Given the following matrix:
[
    [ 1, 2, 3 ],
    [ 4, 5, 6 ],
    [ 7, 8, 9 ]
]
You should return
[1, 2, 3, 6, 9, 8, 7, 4, 5]
"""


def iterate(matrix):
    for row_id, row in enumerate(matrix):
        if row_id % 2 == 0:
            print(row)
        else:
            print(row[::-1])


if __name__ == "__main__":
    mx = [ [ 1, 2, 3 ], [ 4, 5, 6 ], [ 7, 8, 9 ]]
    iterate(mx)
