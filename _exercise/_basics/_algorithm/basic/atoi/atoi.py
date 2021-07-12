
def a2i(number_str):
    def _init_char_map():
        c_map = dict()
        for i in range(10):
            c_map[str(i)] = i
        return c_map

    n_str = number_str.strip() if number_str else None
    if not n_str:
        return None

    sign = -1 if n_str[0] == '-' else 1
    n_str = n_str.lstrip("-").lstrip("+")

    char_map = _init_char_map()
    n = 0
    for c in n_str:
        i = char_map[c] # will throw exception if col is not in map
        n = n * 10 + i
    return n * sign


if __name__ == "__main__":
    for a in ["123", "-123", "+123"]:
        print(f"\"{a}\" => {a2i(a)}")
