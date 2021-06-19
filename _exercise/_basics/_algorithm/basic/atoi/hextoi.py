
def hextoi(number_str):
    def _init_char_map():
        c_map = dict()
        for i in range(10):
            c_map[str(i)] = i
        for i in range(10, 17):
            c_map[chr(i - 10 + ord("A"))] = i
        return c_map

    n_str = number_str.strip() if number_str else None
    if not n_str:
        return None

    sign = -1 if n_str[0] == '-' else 1
    n_str = n_str.lstrip("-").lstrip("+")

    char_map = _init_char_map()
    n = 0
    for c in n_str:
        i = char_map[c]
        n = n * 16 + i
    return n * sign


if __name__ == "__main__":
    for a, i in [("A", 10), ("10", 16), ("1A", 26)]:
        print(f"\"({a}, {i})\" => {hextoi(a)}")
