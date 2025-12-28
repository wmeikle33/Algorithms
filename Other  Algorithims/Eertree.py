from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Node:
    length: int
    link: int
    next: Dict[str, int] = field(default_factory=dict)
    occ: int = 0          # occurrences as a suffix during insertion
    first_pos: int = -1   # ending index of first occurrence (to reconstruct substring)


class Eertree:
    """
    Palindromic Tree (Eertree)
    Stores all DISTINCT palindromic substrings of a string in O(n).
    """

    def __init__(self) -> None:
        self.s: List[str] = []
        # Two roots:
        # node 0: length = -1 (imaginary), link to itself
        # node 1: length = 0  (empty),     link to node 0
        self.nodes: List[Node] = [
            Node(length=-1, link=0),
            Node(length=0, link=0),
        ]
        self.suff = 1  # node index of longest palindromic suffix of current string

    def _get_link(self, v: int, pos: int) -> int:
        """Follow suffix links until we can extend by s[pos]."""
        while True:
            L = self.nodes[v].length
            left = pos - 1 - L
            if left >= 0 and self.s[left] == self.s[pos]:
                return v
            v = self.nodes[v].link

    def add_char(self, ch: str) -> int:
        """
        Add one character to the eertree.
        Returns the node index representing the longest palindromic suffix after insertion.
        """
        self.s.append(ch)
        pos = len(self.s) - 1

        cur = self._get_link(self.suff, pos)

        # If palindrome already exists, just move suff
        if ch in self.nodes[cur].next:
            self.suff = self.nodes[cur].next[ch]
            self.nodes[self.suff].occ += 1
            return self.suff

        # Create new node
        new_len = self.nodes[cur].length + 2
        new_node = Node(length=new_len, link=0, first_pos=pos)
        self.nodes.append(new_node)
        new_id = len(self.nodes) - 1

        self.nodes[cur].next[ch] = new_id

        # Set suffix link of new node
        if new_len == 1:
            # Single character palindromes link to empty palindrome
            self.nodes[new_id].link = 1
        else:
            link_candidate = self._get_link(self.nodes[cur].link, pos)
            self.nodes[new_id].link = self.nodes[link_candidate].next[ch]

        self.suff = new_id
        self.nodes[new_id].occ += 1
        return new_id

    def build(self, s: str) -> None:
        for ch in s:
            self.add_char(ch)

    def distinct_pal_count(self) -> int:
        # exclude the two roots
        return len(self.nodes) - 2

    def propagate_occurrences(self) -> None:
        """
        After building, propagate occurrence counts from longer palindromes to their suffix links.
        This turns 'occ as suffix during insertion' into 'total occurrences in the string'.
        """
        order = sorted(range(2, len(self.nodes)), key=lambda i: self.nodes[i].length, reverse=True)
        for v in order:
            link = self.nodes[v].link
            self.nodes[link].occ += self.nodes[v].occ

    def longest_palindrome(self) -> str:
        best_id = max(range(2, len(self.nodes)), key=lambda i: self.nodes[i].length, default=1)
        L = self.nodes[best_id].length
        if L <= 0:
            return ""
        end = self.nodes[best_id].first_pos
        start = end - L + 1
        return "".join(self.s[start:end + 1])

    def list_distinct_palindromes_with_counts(self) -> List[Tuple[str, int]]:
        """
        Requires propagate_occurrences() called first for correct totals.
        Returns list of (palindrome_string, total_occurrences).
        """
        out = []
        for i in range(2, len(self.nodes)):
            L = self.nodes[i].length
            end = self.nodes[i].first_pos
            start = end - L + 1
            pal = "".join(self.s[start:end + 1])
            out.append((pal, self.nodes[i].occ))
        return out
