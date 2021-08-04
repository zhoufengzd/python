# Trie or prefix tree
#   back tracking: allowed + rollback + process_node

class Node:
    def __init__(self, c=None):
        self.char = c
        self.children = dict()
        self.word_end = False
        self.hit_count = 0
        self.depth = -1     # note: root is depth -1 since it does not hold any char


class Context:
    def __init__(self):
        self.visited = list()


class Trie:
    def __init__(self):
        self.root = Node(None)

    def add(self, word_str):
        curr = self.root
        depth = 0
        for c in word_str:
            curr = curr.children.setdefault(c, Node(c))
            curr.hit_count += 1
            curr.depth = depth
            depth += 1
        curr.word_end = True

    def allowed(self, node, ctxt):
        if not node:
            return False

        if node.depth == -1:  # root
            return True

        if not self.addition_check(node, ctxt):
            return False
        return True

    def next_nodes(self, node, ctxt):
        return node.children.values()

    def traverse(self, node, ctxt):
        if not self.allowed(node, ctxt):
            return

        ctxt.visited.append(node)
        self.process_node(node, ctxt)
        for nd in self.next_nodes(node, ctxt):
            self.traverse(nd, ctxt)
        ctxt.visited.pop()  # rollback

    def addition_check(self, node, ctxt):
        return True

    def process_node(self, node, ctxt):
        pass



if __name__ == "__main__":
    t = Trie()
    for wd in ["the", "a", "there", "answer", "any", "by", "bye", "their"]:
        t.add(wd)

    ct = Context()
    t.traverse(t.root, ct)
