def swap_word_and_case(input_str):
    words = input_str.split()
    words_rev = " ".join([w.swapcase() for w in reversed(words) if w])
    print(words_rev)

if __name__ == "__main__":
    input_str = input()
    swap_word_and_case(input_str)
