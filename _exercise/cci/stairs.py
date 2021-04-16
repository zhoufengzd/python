"""

"""
def run_stairs_recursive(n):
    if n == 0 or n == 1:
        return 1
    elif n == 2:
        return 2    # 2, 1->1
    else:
        return run_stairs_recursive(n-3) + run_stairs_recursive(n-2) + run_stairs_recursive(n-1)

def run_stairs_dynamic(n):
    s = dict()
    s[0] = 1
    s[1] = 1
    s[2] = 2
    for i in range (3, n+1):
        s[i] = s[i-3] + s[i-2] + s[i-1]
    return s[i]


if __name__ == "__main__":
    n = int(input())
    # print(run_stairs_recursive(n))
    print(run_stairs_dynamic(n))
