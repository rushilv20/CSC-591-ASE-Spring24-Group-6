from util import coerce
import math

class NUM:
    def __init__(self, s=None, n=None):
        self.txt = s or " "
        self.at = n or 0
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = float("-inf")
        self.lo = float("inf")
        self.heaven = 0 if s and s.endswith("-") else 1

    def add(self, x):
        if not x == "?":
            x = coerce(x)
            self.n += 1
            d = x - self.mu
            self.mu += d / self.n
            self.m2 += d * (x - self.mu)
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1))**0.5

    def like(self, x, prior=None):
            mu, sd = self.mid(), (self.div() + 1E-30)
            num = math.exp(-0.5 * (x - mu) ** 2 / (sd ** 2))
            denum = (sd * 2.5 + 1E-30)
            return num / denum