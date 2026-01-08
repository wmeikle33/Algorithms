from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
import heapq

INF = 10**18

@dataclass
class Edge:
    to: int
    rev: int          # index of reverse edge in graph[to]
    cap: int
    cost: int

class MinCostMaxFlow:
    def __init__(self, n: int):
        self.n = n
        self.g: List[List[Edge]] = [[] for _ in range(n)]

    def add_edge(self, fr: int, to: int, cap: int, cost: int) -> None:
        """Add directed edge fr->to and residual reverse edge."""
        fwd = Edge(to=to, rev=len(self.g[to]), cap=cap, cost=cost)
        rev = Edge(to=fr, rev=len(self.g[fr]), cap=0, cost=-cost)
        self.g[fr].append(fwd)
        self.g[to].append(rev)

    def min_cost_flow(self, s: int, t: int, maxf: int) -> Tuple[int, int]:
        """
        Returns (flow_sent, min_cost) sending up to maxf flow from s to t.
        If flow_sent < maxf, not enough capacity to send all requested flow.
        """
        n = self.n
        pot = [0] * n  # Johnson potentials
        flow = 0
        cost = 0

        # If you have negative costs initially, you should run Bellman-Ford once
        # to initialize potentials. Many assignment problems have nonnegative costs,
        # so we skip that here for simplicity.

        while flow < maxf:
            dist = [INF] * n
            prev_v = [-1] * n
            prev_e = [-1] * n

            dist[s] = 0
            pq = [(0, s)]
            while pq:
                d, v = heapq.heappop(pq)
                if d != dist[v]:
                    continue
                for ei, e in enumerate(self.g[v]):
                    if e.cap <= 0:
                        continue
                    # reduced cost with potentials: nonnegative if pot is valid
                    nd = d + e.cost + pot[v] - pot[e.to]
                    if nd < dist[e.to]:
                        dist[e.to] = nd
                        prev_v[e.to] = v
                        prev_e[e.to] = ei
                        heapq.heappush(pq, (nd, e.to))

            if prev_v[t] == -1:  # no augmenting path
                break

            # update potentials
            for v in range(n):
                if dist[v] < INF:
                    pot[v] += dist[v]

            # find bottleneck capacity on the path
            addf = maxf - flow
            v = t
            while v != s:
                pv = prev_v[v]
                pe = prev_e[v]
                addf = min(addf, self.g[pv][pe].cap)
                v = pv

            # apply augmentation
            v = t
            while v != s:
                pv = prev_v[v]
                pe = prev_e[v]
                e = self.g[pv][pe]
                e.cap -= addf
                self.g[v][e.rev].cap += addf
                cost += addf * e.cost
                v = pv

            flow += addf

        return flow, cost
