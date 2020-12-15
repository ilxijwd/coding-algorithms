class Node:
    def __init__(self, children):
        self._children = children

    def children(self):
        return self._children

    def value(self):
        return sum(child.value() for child in self._children)


class LeafNode(Node):
    def __init__(self, value, letter):
        self._letter = letter
        self._value = value

    def children(self):
        return []

    def value(self):
        return self._value

    def letter(self):
        return self._letter


def huffman_unpack(k, node):
    if len(node.children()) > 0:
        result = []
        for i, letter in enumerate(node.children()):
            o = huffman_unpack(k + str(i), letter)
            if type(o) == tuple:
                result.append(o)
            else:
                result += o
        return result
    else:
        return k, node.letter()


def huffman_code(letters):
    letters = list(map(list, letters.items()))
    queue = []
    for letter in letters:
        queue.append(LeafNode(letter[1], letter[0]))

    while len(queue) > 1:
        queue.sort(key=lambda i: i.value(), reverse=True)
        a = queue.pop()
        b = queue.pop()
        n = Node([a, b])
        queue.insert(0, n)

    appearance_map = huffman_unpack('', queue[0])
    codes = {}
    for appearance in appearance_map:
        codes[appearance[1]] = appearance[0]

    return codes
