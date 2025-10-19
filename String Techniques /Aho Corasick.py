from collections import deque

class AhoCorasick:
    def __init__(self):
        self.next = [dict()]   
        self.fail = [0] 
        self.out  = [[]]       
        self.pats = []         
        self.len  = []     

    def add(self, pat: str, pid=None):
        if pid is None:
            pid = len(self.pats)
            self.pats.append(pat)
            self.len.append(len(pat))
        s = 0
        for ch in pat:
            if ch not in self.next[s]:
                self.next[s][ch] = len(self.next)
                self.next.append({})
                self.fail.append(0)
                self.out.append([])
            s = self.next[s][ch]
        self.out[s].append(pid)

    def build(self):
        q = deque()
        # depth-1 fail links = 0
        for ch, v in self.next[0].items():
            self.fail[v] = 0
            q.append(v)
        while q:
            u = q.popleft()
            for ch, v in self.next[u].items():
                f = self.fail[u]
                while f and ch not in self.next[f]:
                    f = self.fail[f]
                self.fail[v] = self.next[f].get(ch, 0)
                self.out[v].extend(self.out[self.fail[v]])
                q.append(v)

    def finditer(self, text: str):
        s = 0
        for i, ch in enumerate(text):
            while s and ch not in self.next[s]:
                s = self.fail[s]
            s = self.next[s].get(ch, 0)
            if self.out[s]:
                for pid in self.out[s]:
                    L = self.len[pid]
                    yield (i - L + 1, i, pid, self.pats[pid])

