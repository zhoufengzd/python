# fill in 3 * n spaces with dominos (2 x 1)
# possible shapes of sub area:
#   complete + 1 space left + 2 unconnected spaces left
# reference: https://www.geeksforgeeks.org/tiling-with-dominoes/

##: requires quite some observation!
def countWays(n):
    A = [0] * (n + 1)
    B = [0] * (n + 1)
    A[0] = 1
    A[1] = 0
    B[0] = 0
    B[1] = 1
    for i in range(2, n+1):
        A[i] = A[i - 2] + 2 * B[i - 1]
        B[i] = A[i - 1] + B[i - 2]

    return A[n]

n = 8
print(countWays(n))