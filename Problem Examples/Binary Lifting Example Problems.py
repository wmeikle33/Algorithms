class LCA:
  def __init__(self, n, edges, root = 1:
    self.n = n
    self.Log = (n).bit_length()
    self.adj = [[] for _ in range(n+1)]
    for u,v in edges:
      self.adj[u].append(v)
      self.adj[v].append(u)
    self.depth = [0] * (n+1)
    self.up = [[0] * self.LOG for _ in range(n + 1)] 
    self._build(root)

def _build(self, root):
  self.up[root][0] = root
  for i in range(1, self.LOG):
    self.up[root][i] = root
  stack = [(root,0)]
