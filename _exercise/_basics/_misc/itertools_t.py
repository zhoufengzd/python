# * iterate tools
# * -- https://docs.python.org/3/library/itertools.html
import itertools

# data
letters = ["a", "b", "c", "d", "e", "f"]
booleans = [True, False, True, False, False, True]
numbers = [23, 20, 44, 32, 7, 12]
decimals = [0.1, 0.7, 0.4]

# cypresstunnel@gmail.com kc9Umfb52qRZxT4
def chain_t():
    chained = list(itertools.chain(letters, booleans, decimals))
    letters.append("g") # will not affect the chained output
    print(chained)


def count_t():
    itertools.count(10, 0.25)


if __name__ == "__main__":
    chain_t()
