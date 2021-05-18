
import numpy as np

def reshape():
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    newarr = arr.reshape(4, 3)
    print(newarr)

def concat():
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    arr = np.concatenate((arr1, arr2))
    print(arr)

def sort():
    arr = np.array([3, 2, 0, 1])
    print(np.sort(arr))

def ufunc_add():
    x = [1, 2, 3, 4]
    y = [4, 5, 6, 7]
    z = np.add(x, y)
    print(z)

def ufunc_lcm():
    arr = np.array([3, 6, 9])
    x = np.lcm.reduce(arr)
    print(x)

def ufunc_gcd():
    arr = np.array([3, 6, 9])
    x = np.gcd.reduce(arr)
    print(x)

if __name__ == "__main__":
    # reshape()
    # concat()
    # sort()
    # ufunc_add()
    # ufunc_lcm()
    ufunc_gcd()
