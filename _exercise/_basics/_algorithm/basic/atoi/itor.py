# int to roman numbers
#   roman number is 5 based with hack 10 based chars
def itor(num):
     # Storing roman values of digits from 0-9
     # when placed at different places
     m = [ "", "M", "MM", "MMM" ]
     c = [ "", "C", "CC", "CCC", "CD", "D",
           "DC", "DCC", "DCCC", "CM "]
     x = [ "", "X", "XX", "XXX", "XL", "L",
           "LX", "LXX", "LXXX", "XC" ]
     i = [ "", "I", "II", "III", "IV", "V",
           "VI", "VII", "VIII", "IX"]

     # Converting to roman
     thousands = m[num // 1000]
     hundereds = c[(num % 1000) // 100]
     tens =  x[(num % 100) // 10]
     ones = i[num % 10]

     ans = (thousands + hundereds +
                 tens + ones)

     return ans;

def itor2(n):
    def _init_char_map():
        c_map = {1: "I", 5:"V", 10:"X", 50: "L", 100:"C", 500:"D", 1000: "M"}
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
        print(f"{i} => \"{itor(i)}\"")
