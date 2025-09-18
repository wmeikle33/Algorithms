class Trie:
    __slots__ = ("children", "end")
    def __init__(self):
        self.children = {}
        self.end = False

class PrefixTrie:
    def __init__(self):
        self.root = Trie()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return bool(node and node.end)

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s: str):
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if not node:
                return None
        return node
