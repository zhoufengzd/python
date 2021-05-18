
def a2i(number_str):
    """assume good numbers, either positive 123, or negative -123. """
    n_str = number_str.strip() if number_str else None
    if not n_str:
        return None

    sign = -1 if n_str[0] == '-' else 1
    n_str = n_str.lstrip("-").lstrip("+")

    n = 0
    for idx in range(len(n_str)):
        i = ord(n_str[idx]) - ord('0')
        if i > 9 or i < 0:
            return None

        n = n * 10 + i
    return n * sign


if __name__ == "__main__":
    for s in ["123", "-123", "+123", " x "]:
        print("{} => {}".format(s, a2i(s)))
