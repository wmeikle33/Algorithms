from collections import defaultdict
import sys
sys.setrecursionlimit(10**7)

def dsu_on_tree_example(n, parent, color):
    """
    n: number of nodes (1..n)
    parent[i]: parent of i (i>=2), parent[1] ignored
    color[i]: color of i (1-indexed)
    returns: ans[v] = max frequency of any color in subtree of v
    """
    g = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        g[parent[v]].append(v)

    # postorder to avoid recursion if you want, but recursion is fine here
    size = [0] * (n + 1)
    heavy = [0] * (n + 1)

    def dfs_sz(v):
        size[v] = 1
        mx = 0
        for u in g[v]:
            dfs_sz(u)
            size[v] += size[u]
            if size[u] > mx:
                mx = size[u]
                heavy[v] = u

    dfs_sz(1)

    ans = [0] * (n + 1)
    # maps[v] will store color counts for subtree v (but we keep only for "kept" nodes)
    maps = [None] * (n + 1)

    def add_map(dst, src):
        # merge src into dst (small-to-large)
        for k, val in src.items():
            dst[k] += val

    def dfs(v):
        # process light children first (their maps will be discarded)
        for u in g[v]:
            if u != heavy[v]:
                dfs(u)

        # process heavy child last and keep its map
        if heavy[v]:
            dfs(heavy[v])
            maps[v] = maps[heavy[v]]
        else:
            maps[v] = defaultdict(int)

        # add v itself
        maps[v][color[v]] += 1

        # merge light children maps into maps[v]
        for u in g[v]:
            if u == heavy[v]:
                continue
            add_map(maps[v], maps[u])

        # compute answer for v from its map
        ans[v] = max(maps[v].values())

    dfs(1)
    return ans[1:]
