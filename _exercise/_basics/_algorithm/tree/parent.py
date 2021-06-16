# Tree iteration with parent node memerized
# assumption:
#   * directed graph (parent => children only)
class Node:
    def __init__(self, id):
        self.id = id
        self.children = list()

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)


def findParent(root, child_id):
    from collections import deque

    def add_child(node, targets):
        for child in node.children:
            targets.append((child, node))

    # bfs: queue (FIFO) and remember each child's parent in iteration
    targets = deque()
    add_child(root, targets)
    while list(targets):
        pair = targets.popleft()
        if pair[0].id == child_id:
            return pair[1]
        add_child(pair[0], targets)
    return Node(-1)


if __name__ == "__main__":
    nodes = dict()
    for i in range(6):
        nodes[i] = Node(i)
    nodes[0].children = [nodes[1], nodes[2]]
    nodes[1].children = [nodes[3], nodes[4]]
    nodes[2].children = [nodes[5]]

    for dt in [5, 0, 1]:
        node = findParent(nodes[0], dt)
        print(f"{dt} ? {node.id:3}")
