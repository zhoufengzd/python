#!/usr/bin/env python

import math
import os
import random
import re
import sys

def fizzBuzz(n):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

if __name__ == "__main__":
    input_str = input()
    try:
        max_n = int(input_str)
        for i in range(1, max_n+1):
            fizzBuzz(i)
    except Exception as e:
        print(e)
