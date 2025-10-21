def dijkstra(n: int, adj: List[List[Tuple[int, int]]], src: int):
    """
    n   : number of nodes (0..n-1)
    adj : adjacency list; adj[u] = [(v, w), ...] with edge weight w >= 0
    src : source node
    Returns (dist, parent):
      dist[v]   = shortest distance from src to v (inf if unreachable)
      parent[v] = previous node on a shortest path (or -1 for src/unreachable)
    """
    INF = float('inf')
    dist = [INF] * n
    parent = [-1] * n
    dist[src] = 0
    pq = [(0, src)]  # (distance so far, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:          # stale entry
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent
