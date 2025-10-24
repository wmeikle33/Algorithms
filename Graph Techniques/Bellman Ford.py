from collections import deque
from math import inf
from typing import List, Tuple, Optional, Set

def bellman_ford(n: int, edges: List[Tuple[int, int, int]], src: int):
    dist = [inf] * n
    parent = [-1] * n
    dist[src] = 0

    # Relax edges up to n-1 times
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break

    # Build adjacency to propagate "negative cycle influence"
    adj = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)

    # Detect nodes that can still be relaxed -> on or reachable from a negative cycle
    neg_cycle_nodes: Set[int] = set()
    queue = deque()
    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            if v not in neg_cycle_nodes:
                neg_cycle_nodes.add(v)
                queue.append(v)

    # Propagate to everything reachable from those nodes
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if y not in neg_cycle_nodes:
                neg_cycle_nodes.add(y)
                queue.append(y)

    # Mark distances of affected nodes as -inf
    for v in neg_cycle_nodes:
        dist[v] = float('-inf')

    return dist, parent, neg_cycle_nodes


def reconstruct_path(parent: List[int], t: int) -> Optional[List[int]]:
    """Reconstruct path to t using parent[] (returns None if unreachable)."""
    if parent[t] == -1 and t != 0:  # adjust if your source isn't 0
        return None
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]
