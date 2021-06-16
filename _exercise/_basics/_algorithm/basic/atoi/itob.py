
def itob(n):
    def _init_char_map():
        c_map = dict()
        for i in range(2):
            c_map[i] = chr(i + ord("0"))
        return c_map

    if n == 0:
        return "0"

    char_map = _init_char_map()
    result = ""
    while n:
        remainder = n % 2
        result += char_map[remainder]
        n = n //2
    return result[::-1]


if __name__ == "__main__":
    for i in range(10):
        print(f"{i} => \"{itob(i)}\"")
