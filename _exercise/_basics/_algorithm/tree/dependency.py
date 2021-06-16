# Graph depth first iteration
#   * checking circular dependencies
#   * build leaf to root list
# assumption:
#   * directed graph (parent => children only)
#   * value is unique / the identifier in the tree
#   *
class Node:
    def __init__(self, id):
        self.id = id
        self.edges = list()

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.id)


def _iterate(root):
    # dfs: stack (FILO)
    result = list()
    visited = set()

    targets = list()
    targets.append(root)
    while targets:
        node = targets.pop()
        if node in result:
            # refresh the sequence
            result.remove(node)
            result.append(node)
        else:
            # new node
            if node in visited:
                print(f"{node} visited. circular dependencies found.")
                return list()
            targets.extend(node.edges)
            result.append(node)
    return result[::-1]  # build order: reverse the list (leaf first)


def dep_resolve(node, result, seen):
    # print(node.id)
    seen.append(node)
    for nd in node.edges:
        # if nd in result:
        #     # refresh the sequence
        #     result.remove(node)
        #     result.append(node)
        if nd not in result: #else:
            if nd in seen:
                raise Exception('Circular reference detected: %s -> %s' % (str(node.id), str(nd.id)))
            dep_resolve(nd, result, seen)
    result.append(node)


if __name__ == "__main__":
    nodes = dict()
    for i in range(6):
        nodes[i] = Node(i)
    nodes[0].edges.extend([nodes[1], nodes[2]])
    nodes[1].edges.extend([nodes[3], nodes[4]])
    nodes[2].edges.extend([nodes[4], nodes[5]])
    # nodes[5].edges.extend([nodes[0]])  # circular

    # for dt in [6]:
    #     res = _iterate(nodes[0])
    #     print(" ".join([str(e) for e in res]))

    res = []
    dep_resolve(nodes[0], res, [])
    print(" ".join([str(e) for e in res]))
