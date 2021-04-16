def is_leap(n):
    if n % 400 == 0:
        return True
    elif n % 100 == 0:
        return False
    else:
        return (True if n % 4 == 0 else False)


if __name__ == "__main__":
    n = int(input().strip())
    print(is_leap(n))
