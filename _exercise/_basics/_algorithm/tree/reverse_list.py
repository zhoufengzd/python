# reverse a linked list

class Node:
    def __init__(self, id, next):
        self.id = id
        self.next = next
    def __str__(self):
        return str(self.id)


def build_linked(node_count):
    curr = prev = None
    for i in range(node_count, 0, -1):
        curr = Node(i, prev)
        prev = curr
    return curr


def print_linked(root):
    result = list()
    curr = root
    while curr:
        result.append(str(curr))
        curr = curr.next
    print(" -> ".join(result))


def reverse_linked(root):
    prev = next = None
    curr = root
    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev


def dfs(prev, curr):
    if not curr:
        return prev

    next = curr.next
    curr.next = prev
    return dfs(curr, next)


if __name__ == "__main__":
    root = build_linked(4)
    print_linked(root)
    # root = reverse_linked(root)
    root = dfs(None, root)
    print_linked(root)
