# There are 100 doors, all closed. In a nearby cage are 100 monkeys.
# The first monkey is let out, and runs along the doors opening every one.
# The second monkey is then let out, and runs along the doors closing the door 2, 4, 6...
# The third monkey is let out, and he attends only to the 3rd, 6th, 9th, and toggle the door state
# After all 100 monkeys have done their work in this way, which doors are left open?
# door(n) = touched if n % monkey_id = 0

# observe the factors(n). If even number of monkeys touch the door, door will be closed at the end.
# only if n is perfect square, then sqrt(n) is only added once, odd number of monkeys touch the door.
def factors(n):
    import math
    res = list()
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            res.append(i)
            if i != n // i: # not square root
                res.append(n // i)
    return sorted(res)


if __name__ == "__main__":
    for dt in [1, 2, 4, 7, 10, 100]:
        result = factors(dt)
        print(f"{dt} -> {len(result)}: {result}")
