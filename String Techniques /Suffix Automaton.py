class SuffixAutomaton:
    def __init__(self, s: str = ""):
        self.next = []       # list[dict(char->state)]
        self.link = []       # list[int]
        self.length = []     # list[int]
        self.occ = []        # endpos size (to be propagated)
        self.first_pos = []  # first end position in original string
        self.last = 0        # current last state
        self._init_state()
        self.s = ""
        if s:
            self.build(s)

    def _init_state(self):
        self.next.append({})
        self.link.append(-1)
        self.length.append(0)
        self.occ.append(0)
        self.first_pos.append(-1)

    def add_char(self, c: str, idx: int):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)
        self.occ.append(1)               # each new terminal contributes 1
        self.first_pos.append(idx)       # ends at idx
        p = self.last
        while p >= 0 and c not in self.next[p]:
            self.next[p][c] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                # clone q
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])
                self.occ.append(0)                 # clones don't start as terminals
                self.first_pos.append(self.first_pos[q])
                while p >= 0 and self.next[p].get(c) == q:
                    self.next[p][c] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

    def build(self, s: str):
        self.__init__("")  # reset to empty SAM
        self.s = s
        for i, ch in enumerate(s):
            self.add_char(ch, i)
        self._propagate_occ()

    def _propagate_occ(self):
        # topologically order states by length descending
        order = sorted(range(len(self.next)), key=self.length.__getitem__, reverse=True)
        for v in order:
            if self.link[v] != -1:
                self.occ[self.link[v]] += self.occ[v]

    # --- Queries ---

    def contains(self, pat: str) -> bool:
        v = 0
        for ch in pat:
            if ch not in self.next[v]:
                return False
            v = self.next[v][ch]
        return True

    def count_occurrences(self, pat: str) -> int:
        v = 0
        for ch in pat:
            if ch not in self.next[v]:
                return 0
            v = self.next[v][ch]
        return self.occ[v]

    def distinct_substrings(self) -> int:
        # sum over states: len[v] - len[link[v]]
        total = 0
        for v in range(1, len(self.next)):     # skip state 0 (link = -1)
            total += self.length[v] - self.length[self.link[v]]
        return total

    def longest_common_substring(self, t: str):
        """Return (length, substring) of LCS between self.s and t."""
        v = 0
        l = 0
        best = (0, -1)  # (length, end_pos_in_self)
        for ch in t:
            while v and ch not in self.next[v]:
                v = self.link[v]
                l = self.length[v]
            if ch in self.next[v]:
                v = self.next[v][ch]
                l += 1
            else:
                v = 0
                l = 0
            if l > best[0]:
                best = (l, self.first_pos[v])
        L, end = best
        substr = self.s[end - L + 1:end + 1] if L > 0 else ""
        return L, substr
