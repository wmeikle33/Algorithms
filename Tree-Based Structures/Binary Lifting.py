class LCA:
    def __init__(self, n, edges, root=1):
        self.n = n
        self.LOG = (n).bit_length()
        self.adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.depth = [0] * (n + 1)
        self.up = [[0] * self.LOG for _ in range(n + 1)]  # up[v][i] = 2^i-th ancestor of v
        self._build(root)

    def _build(self, root):
        # iterative DFS so parent is processed before child
        self.up[root][0] = root
        for i in range(1, self.LOG):
            self.up[root][i] = root

        stack = [(root, 0)]  # (node, parent)
        while stack:
            u, p = stack.pop()
            if p:
                self.depth[u] = self.depth[p] + 1
                self.up[u][0] = p
                for i in range(1, self.LOG):
                    self.up[u][i] = self.up[self.up[u][i - 1]][i - 1]
            for v in self.adj[u]:
                if v == p:
                    continue
                stack.append((v, u))

    def kth_ancestor(self, u, k):
        for i in range(self.LOG):
            if k & (1 << i):
                u = self.up[u][i]
        return u

    def lca(self, a, b):
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        # lift a up to depth of b
        a = self.kth_ancestor(a, self.depth[a] - self.depth[b])
        if a == b:
            return a
        # jump both up while their ancestors differ
        for i in range(self.LOG - 1, -1, -1):
            if self.up[a][i] != self.up[b][i]:
                a = self.up[a][i]
                b = self.up[b][i]
        return self.up[a][0]

    def dist(self, a, b):
        c = self.lca(a, b)
        return self.depth[a] + self.depth[b] - 2 * self.depth[c]

    def kth_on_path(self, a, b, k):
        """
        0-based: k=0 returns a; k=dist(a,b) returns b.
        """
        c = self.lca(a, b)
        da = self.depth[a] - self.depth[c]
        if k <= da:
            return self.kth_ancestor(a, k)
        # go from c down to b
        db = self.depth[b] - self.depth[c]
        k2 = da + db - k
        return self.kth_ancestor(b, k2)
