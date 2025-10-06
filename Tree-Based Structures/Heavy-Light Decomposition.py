class SegTree:
    def __init__(self, arr):
        self.n = len(arr) - 1                   
        self.seg = [0] * (4 * self.n)
        self._build(arr, 1, 1, self.n)

    def _build(self, a, idx, l, r):
        if l == r:
            self.seg[idx] = a[l]
            return
        m = (l + r) // 2
        self._build(a, idx*2, l, m)
        self._build(a, idx*2+1, m+1, r)
        self.seg[idx] = self.seg[idx*2] + self.seg[idx*2+1]

    def update(self, pos, val, idx=1, l=1, r=None):
        if r is None: r = self.n
        if l == r:
            self.seg[idx] = val
            return
        m = (l + r) // 2
        if pos <= m: self.update(pos, val, idx*2, l, m)
        else:        self.update(pos, val, idx*2+1, m+1, r)
        self.seg[idx] = self.seg[idx*2] + self.seg[idx*2+1]

    def query(self, ql, qr, idx=1, l=1, r=None):
        if r is None: r = self.n
        if qr < l or r < ql: return 0
        if ql <= l and r <= qr: return self.seg[idx]
        m = (l + r) // 2
        return self.query(ql, qr, idx*2, l, m) + self.query(ql, qr, idx*2+1, m+1, r)

class HLD:
    def __init__(self, n, edges, values, root=1):
        self.n = n
        self.adj = [[] for _ in range(n+1)]
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.parent = [0]*(n+1)
        self.depth  = [0]*(n+1)
        self.size   = [0]*(n+1)
        self.heavy  = [-1]*(n+1)

        self.head = [0]*(n+1)   
        self.pos  = [0]*(n+1)   
        self.timer = 0

        self.values = values[:] 

        self._dfs1(root, 0)
        self.base = [0]*(n+1)
        self._dfs2(root, root)
        for u in range(1, n+1):
            self.base[self.pos[u]] = self.values[u]
        self.st = SegTree(self.base)

    def _dfs1(self, u, p):
        self.parent[u] = p
        self.depth[u] = self.depth[p] + 1 if p else 0
        self.size[u] = 1
        max_sz = 0
        for v in self.adj[u]:
            if v == p: continue
            self._dfs1(v, u)
            self.size[u] += self.size[v]
            if self.size[v] > max_sz:
                max_sz = self.size[v]
                self.heavy[u] = v

    def _dfs2(self, u, h):
        self.head[u] = h
        self.timer += 1
        self.pos[u] = self.timer
        if self.heavy[u] != -1:
            self._dfs2(self.heavy[u], h)  # continue heavy path
            for v in self.adj[u]:
                if v != self.parent[u] and v != self.heavy[u]:
                    self._dfs2(v, v)      # start new heavy path

    def query_path(self, u, v):
        res = 0
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            res += self.st.query(self.pos[self.head[u]], self.pos[u])
            u = self.parent[self.head[u]]
        # now same head; ensure u is above v
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        res += self.st.query(self.pos[u], self.pos[v])
        return res

    def update_point(self, u, new_val):
        self.st.update(self.pos[u], new_val)

    def query_subtree(self, u):
        l = self.pos[u]
        r = self.pos[u] + self.size[u] - 1
        return self.st.query(l, r)
