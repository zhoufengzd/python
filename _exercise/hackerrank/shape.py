#!/usr/bin/env python

import math
import os
import random
import re
import sys


class Rectangle:
    def __init__(self, width, length):
        self.width = width
        self.length = length
    def area(self):
        return round(self.width * self.length, 2)

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return round(math.pi * (self.radius * self.radius), 2)


if __name__ == "__main__":
    test_cases = 0
    for line in sys.stdin.readlines():
        if not test_cases:
            test_cases = int(line)
            continue

        params = line.split()
        if "circle" in line:
            print(Circle(float(params[1])).area())
        elif "rectangle" in line:
            print(Rectangle(float(params[1]), float(params[2])).area())

        test_cases -= 1
        if not test_cases:
            break
