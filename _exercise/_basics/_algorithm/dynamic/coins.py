# sum of ways of coin changes

def get_changes(total, coin_list):
    changes = {s: 0 for s in range(0, total + 1)}
    changes[0] = 1

    # for s in range(coin_list[0], total + 1):
    #     for coin in coin_list:
    #         # if s > coin:    # no need to go further with larger coins
    #         if s == 3:
    #             print(f"s={s}  coin={coin} changes[{s - coin}]={changes[s - coin]}")
    #             # s=3  coin=1 changes[2]=2
    #         if coin <= s:
    #             changes[s] += changes[s - coin]
    for coin in coin_list:
        for s in range(coin_list[0], total + 1):
            # if s == 3:
            #     print(f"s={s}  coin={coin} changes[{s - coin}]={changes[s - coin]}")
                # s=3  coin=1 changes[2]=1
            if coin <= s:    #
                changes[s] += changes[s - coin]
                print(f"s={s}  coin={coin} changes[{s - coin}]={changes[s - coin]}")

    return changes


if __name__ == "__main__":
    coins = [[1, 2, 3]]
    totals = [2]

    for t in totals:
        for c in coins:
            ways = get_changes(t, c)
            print(f"{c} => {t}: {ways}")
