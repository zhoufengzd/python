import math
import os
import random
import re
import sys


if __name__ == '__main__':
    lines = sys.stdin.readlines()
    nm = lines[0].split()
    n = int(nm[0])
    m = int(nm[1])

    # build attribute map: attribute index -> attribute map
    attributes = dict()
    for attribute_idx in range(m):
        attributes[attribute_idx] = dict()

    # full data set in original order. ordinal -> dt_line
    dt = dict()
    for line_id in range(1, n + 1):
        dt_line = lines[line_id].rstrip().split()
        dt[line_id] = dt_line
        for attribute_idx in range(m):
            # attribute_map: attribute -> [line_id]
            attribute_map = attributes[attribute_idx]
            attribute_value = int(dt_line[attribute_idx])
            mapped_lines = attribute_map.get(attribute_value, None)
            if not mapped_lines:
                mapped_lines = list()
                attribute_map[attribute_value] = mapped_lines
            mapped_lines.append(line_id)

    attribute_idx = int(lines[-1])
    attribute_map = attributes[attribute_idx]
    for attribute in sorted(attribute_map.keys()):
        for line_id in attribute_map[attribute]:
            print(' '.join(dt[line_id]))
