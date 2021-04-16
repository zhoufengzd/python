
def is_weird(i):
    if i % 2 == 1:
        print("Weird")
    elif i >= 2 and i <= 5:
        print("Not Weird")
    elif i >= 6 and i <= 20:
        print("Weird")
    else:
        print("Not Weird")

if __name__ == "__main__":
    n = int(input().strip())
    is_weird(n)
