from typing import List, Tuple
import sys
sys.setrecursionlimit(10**7)

def build_adj(n: int, edges: List[Tuple[int,int]]) -> List[List[int]]:
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v); g[v].append(u)
    return g


def subtree_size_and_sum(n: int, edges: List[Tuple[int,int]], val: List[int]) -> Tuple[List[int], List[int]]:
    g = build_adj(n, edges)
    sz = [0]*n           
    ssum = [0]*n        
    
    def dfs(u: int, p: int) -> None:
        sz[u] = 1
        ssum[u] = val[u]
        for v in g[u]:
            if v == p: continue
            dfs(v, u)
            sz[u] += sz[v]
            ssum[u] += ssum[v]

    dfs(0, -1)
    return sz, ssum

def tree_mwis(n: int, edges: List[Tuple[int,int]], w: List[int]) -> int:
    g = build_adj(n, edges)
    dp0 = [0]*n
    dp1 = [0]*n

    def dfs(u: int, p: int) -> None:
        dp1[u] = w[u]
        for v in g[u]:
            if v == p: continue
            dfs(v, u)
            dp0[u] += max(dp0[v], dp1[v])  
            dp1[u] += dp0[v]      

    dfs(0, -1)
    return max(dp0[0], dp1[0])


def tree_diameter(n: int, edges: List[Tuple[int,int]]) -> int:
    g = build_adj(n, edges)
    ans = 0

    def dfs(u: int, p: int) -> int:
        nonlocal ans
        best1 = best2 = 0  
        for v in g[u]:
            if v == p: continue
            h = dfs(v, u) + 1
            if h > best1:
                best2 = best1; best1 = h
            elif h > best2:
                best2 = h
        ans = max(ans, best1 + best2) 
        return best1

    dfs(0, -1)
    return ans

def sum_of_distances_all_nodes(n: int, edges: List[Tuple[int,int]]) -> List[int]:
    g = build_adj(n, edges)
    sz = [1]*n
    down = [0]*n  
    ans = [0]*n

    def dfs1(u: int, p: int) -> None:
        for v in g[u]:
            if v == p: continue
            dfs1(v, u)
            sz[u] += sz[v]
            down[u] += down[v] + sz[v]  

    def dfs2(u: int, p: int) -> None:
        for v in g[u]:
            if v == p: continue
            ans[v] = ans[u] - sz[v] + (n - sz[v])
            dfs2(v, u)

    dfs1(0, -1)
    ans[0] = down[0]
    dfs2(0, -1)
    return ans

