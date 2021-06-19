# Form minimum number from given sequence
# Difficulty Level : Hard
# Last Updated : 04 Jun, 2021
# Given a pattern containing only I’s and D’s. I for increasing and D for decreasing. Devise an algorithm to print the minimum number following that pattern. Digits from 1-9 and digits can’t repeat.

# Examples:

#    Input: D        Output: 21
#    Input: I        Output: 12
#    Input: DD       Output: 321
#    Input: II       Output: 123
#    Input: DIDI     Output: 21435
#    Input: IIDDD    Output: 126543
#    Input: DDIDDIID Output: 321654798

##
def di_pattern(pattern):
    res = list()

    stack = list()
    for i in range(len(pattern) + 1):
        # stack with range of numbers in incremental order
        stack.append(i + 1)

    if (i == len(pattern) or pattern[i] == 'I'):
        # clear numbers from the incremental buffer
        # previous pattern is "D..."
        while len(stack) > 0:
            res.append(stack.pop())

    return res


if __name__ == "__main__":
    # for ptn in ["I", "D", "DD", "II", "IDID", "IIDDD", "DDIDDIID"]:
    for ptn in ["DI"]:
        print(f"{ptn} => {di_pattern(ptn)}")
