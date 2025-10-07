class BIT:
    def __init__(self, n):
        self.n, self.ft = n, [0]*(n+1)
        
    def add(self, i, v):
        while i <= self.n:
            self.ft[i] += v
            i += i & -i
            
    def sum(self, i):
        s = 0
        while i > 0:
            s += self.ft[i]
            i -= i & -i
        return s
