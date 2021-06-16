# currently only support base62 / base64
def itobase6x(n, base):
    def _init_char_map():
        c_map = dict()
        for i in range(0, 26):
            c_map[i] = chr(i + ord("A"))
        for i in range(26, 52):
            c_map[i] = chr(i - 26 + ord("a"))
        for i in range(52, 62):
            c_map[i] = str(i - 52)
        c_map.update({62: "+", 63: "/"})
        return c_map

    if n == 0:
        return "A"

    char_map = _init_char_map()
    result = ""
    while n:
        remainder = n % base
        result += char_map[remainder]
        n = n // base
    return result[::-1]


if __name__ == "__main__":
    for i in range(70):
        print(f"{i} => \"{itobase6x(i, 64)}\"")
