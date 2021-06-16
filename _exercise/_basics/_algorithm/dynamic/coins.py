# sum of ways of coin changes

def get_changes(total, coin_list):
    changes = {s: 0 for s in range(0, total + 1)}
    changes[0] = 1

    for coin in coin_list:
        for s in range(coin, total + 1):
            changes[s] += changes[s - coin]
        print(f"# -- coin = {coin}, changes = {changes}")
    return changes[total]


if __name__ == "__main__":
    coins = [[1, 2]]
    totals = [5]

    for t in totals:
        for c in coins:
            ways = get_changes(t, c)
            print(f"{c} => {t}: {ways}")
