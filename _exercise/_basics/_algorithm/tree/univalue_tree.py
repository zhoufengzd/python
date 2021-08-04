#

class Node:
    def __init__(self, id, tag):
        self.id = id
        self.tag = tag
        self.children = list()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(f"{self.id}({self.tag})")

    def __repr__(self):
        return str(f"{self.id}({self.tag})")


def is_univalue(node, result):
    if not node or not node.children:
        result.append(node)
        return True

    univalue = True
    for child in node.children:
        if not (is_univalue(child, result) and child.tag == node.tag):
            univalue = False
    if univalue:
        result.append(node)
    return univalue


def init_tree():
    nodes = dict()
    nodes[0] = Node(0, "a")
    nodes[1] = Node(1, "b")
    nodes[2] = Node(2, "a")
    nodes[3] = Node(3, "b")
    nodes[4] = Node(4, "b")
    nodes[5] = Node(5, "a")
    nodes[0].children = [nodes[1], nodes[2]]
    nodes[1].children = [nodes[3], nodes[4]]
    nodes[2].children = [nodes[5]]
    return nodes


if __name__ == "__main__":
    nd = init_tree()
    result = list()
    is_univalue(nd[0], result)
    print(result)

