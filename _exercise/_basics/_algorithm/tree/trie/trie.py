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
    def __init__(self, prefix=None):
        self.prefix = prefix
        self.traversed = list()
        self.words = list()


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

        # search
        if node.depth < len(ctxt.prefix):
            return node.char == ctxt.prefix[node.depth]
        return True

    def process_node(self, node, ctxt):
        if node.word_end and node.depth >= (len(ctxt.prefix) - 1):
            ctxt.words.append("".join([nd.char for nd in ctxt.traversed if nd.char]))

    def traverse(self, node, ctxt):
        if not self.allowed(node, ctxt):
            return

        ctxt.traversed.append(node)
        self.process_node(node, ctxt)
        for nd in node.children.values():
            self.traverse(nd, ctxt)
        ctxt.traversed.pop()  # rollback


if __name__ == "__main__":
    t = Trie()
    for wd in ["the", "a", "there", "answer", "any", "by", "bye", "their"]:
        t.add(wd)

    for pre in ["an", "thei"]:
        ct = Context()
        ct.prefix = pre
        t.traverse(t.root, ct)
        print(ct.words)
