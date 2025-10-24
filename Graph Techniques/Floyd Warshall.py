from math import inf
from typing import List, Tuple, Optional

def floyd_warshall(n: int, edges: List[Tuple[int,int,int]]):
    dist = [[inf]*n for _ in range(n)]
    nxt  = [[-1]*n  for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        nxt[i][i] = i
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v]  = v

    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == inf: 
                continue
            di = dist[i]
            nx_i = nxt[i]
            for j in range(n):
                val = dik + dk[j]
                if val < di[j]:
                    di[j] = val
                    nx_i[j] = nx_i[k]

    for k in range(n):
        if dist[k][k] < 0:
            for i in range(n):
                if dist[i][k] == inf: 
                    continue
                for j in range(n):
                    if dist[k][j] == inf:
                        continue
                    dist[i][j] = float('-inf')
                    nxt[i][j]  = -1

    return dist, nxt

def reconstruct_path(u: int, v: int, nxt: List[List[int]], dist: List[List[float]]) -> Optional[List[int]]:
    if dist[u][v] == inf or dist[u][v] == float('-inf') or nxt[u][v] == -1:
        return None
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path
