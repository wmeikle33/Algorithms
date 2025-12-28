from collections import deque
from typing import List, Tuple

def hopcroft_karp(adj: List[List[int]], n_left: int, n_right: int) -> Tuple[int, List[int], List[int]]:
    """
    adj[u] = list of right-vertices v that left-vertex u connects to.
    Left side:  0..n_left-1
    Right side: 0..n_right-1

    Returns:
      matching_size,
      pairU: size n_left, pairU[u] = matched v or -1
      pairV: size n_right, pairV[v] = matched u or -1
    """
    INF = 10**9
    pairU = [-1] * n_left
    pairV = [-1] * n_right
    dist = [0] * n_left

    def bfs() -> bool:
        q = deque()
        for u in range(n_left):
            if pairU[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF

        found_free_right = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                pu = pairV[v]          # matched left node of v (or -1)
                if pu == -1:
                    found_free_right = True
                elif dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
        return found_free_right

    def dfs(u: int) -> bool:
        for v in adj[u]:
            pu = pairV[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pairU[u] = v
                pairV[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in range(n_left):
            if pairU[u] == -1 and dfs(u):
                matching += 1

    return matching, pairU, pairV
