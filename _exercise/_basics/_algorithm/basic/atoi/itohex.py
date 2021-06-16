
def ito_hex(n):
    def _init_char_map():
        c_map = dict()
        for i in range(10):
            c_map[i] = str(i)
        for i in range(10, 17):
            c_map[i] = chr(i - 10 + ord("A"))
        return c_map

    if n == 0:
        return "0"

    char_map = _init_char_map()
    result = ""
    while n:
        remainder = n % 16
        result += char_map[remainder]
        n = n // 16
    return result[::-1]


if __name__ == "__main__":
    for i in range(66):
        print(f"{i} => \"{ito_hex(i)}\"")
