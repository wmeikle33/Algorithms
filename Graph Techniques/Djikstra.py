def dijkstra(n: int, adj: List[List[Tuple[int, int]]], src: int):
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
