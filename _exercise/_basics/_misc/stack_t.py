# Use list
stack = list()

# append() function to push
# element in the stack
stack.append("a")
stack.append("b")
stack.append("col")

print("Initial stack")
print(stack)

# pop() fucntion to pop
# element from stack in
# LIFO order
print("\nElements poped from stack:")
print(stack.pop())
print(stack.pop())
print(stack.pop())

print("\nStack after elements are poped:")
print(stack)
