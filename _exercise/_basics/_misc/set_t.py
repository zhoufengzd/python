
x = {1, 2, 3}
y = x.copy()
print(f"x = {x}; y = x.copy() = {y}")

x.add(4)
print(f"x.add(4) = {x}. No change on y:{y}")

z = {7, 8, 9}
x = x.union(z)
print(f"x | ({z}) = {x | z}")

print(f"x & y: {x & y}")

z.remove(9)
print(f"z.remove(9): {z}")

