
# i to excel column header
def itoaz(n):
    def _init_char_map():
        c_map = dict()
        c_map[0] = "Z"
        for i in range(1, 26):
            c_map[i] = chr(i - 1 + ord("A"))
        return c_map

    if n == 0:
        return "Z"

    char_map = _init_char_map()
    result = ""
    while n:
        remainder = n % 26
        result += char_map[remainder]
        n = n // 26
    return result[::-1]


def itoa(n):
    if n == 0:
        return "0"

    result = ""
    while n:
        remainder = n % 10;
        result += chr(remainder + ord("0"))
        n = n // 10
    return result[::-1]


if __name__ == "__main__":
    for i, a in [(0, "Z"), (1, "A"), (5, "E"), (10, "J"), (26, "Z"), (27, "AA"), (52, "AZ"), (53, "BA"), (702, "ZZ"), (703, "AAA")]:
        # print(f"{i} => \"{itoa(i)}\"")
        print(f"({i, a}) => \"{itoaz(i)}\"")
