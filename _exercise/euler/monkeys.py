# There are 100 doors, all closed. In a nearby cage are 100 monkeys.
# The first monkey is let out, and runs along the doors opening every one.
# The second monkey is then let out, and runs along the doors closing the door 2, 4, 6...
# The third monkey is let out, and he attends only to the 3rd, 6th, 9th, and toggle the door state
# After all 100 monkeys have done their work in this way, which doors are left open?
# door(n) = touched if n % monkey_id = 0

# observe the factors,
#   all odd numbers will remain open since factors(n) = {1... n}
#   all even numbers

def factors(n):
    import math
    res = list()
    res.append(1)
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            res.append(i)
            if i != n // i:
                res.append(n // i)
    res.append(n)
    return sorted(res)


if __name__ == "__main__":
    for dt in [10, 100]
        result = factors(dt)
        print(f"{dt} -> {len(result)}: {result}")
