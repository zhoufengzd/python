def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


def test_infinite_sequence():
    for i in infinite_sequence():
        print(i, end=" ")
        if i > 10000:
            break


def limited_chars(word_str):
    i = 0
    while i < len(word_str):
        yield word_str[i]
        i += 1
    yield None


if __name__ == "__main__":
    # test_infinite_sequence()
    # c =
    for c in limited_chars("abc"):
        # print(f"{i}: {c}")
        print(c)
