# sum of ways of step up stairs

def run_stairs(total, steps):
    steps.sort()
    ways = {s: 0 for s in range(0 - steps[-1], total + 1)}
    ways[0] = 1

    # note: 1->2 is different to 2->1
    for s in range(steps[0], total + 1):
        for step in steps:
            ways[s] += ways[s - step]
            # print(f"# -- step = {step}, ways = {ways}")
    return ways[total]


if __name__ == "__main__":
    steps = [[1, 2]]
    totals = [37]

    for t in totals:
        for st in steps:
            w = run_stairs(t, st)
            print(f"{st} => {t}: {w}")
