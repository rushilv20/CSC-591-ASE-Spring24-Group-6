import math


class ROW:
    def __init__(self, the, cells):
        self.cells = cells
        self.the = the

    def likes(self, datas):
        n, nHypotheses = 0, 0
        for k, data in datas.items():
            n += len(data.rows)
            nHypotheses += 1

        most, out = None, None
        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k
        return out, most

    def like(self, data, n, nHypotheses):
        prior = (len(data.rows) + self.the.k) / (n + self.the.k * nHypotheses)
        out = math.log(prior)

        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                try:
                    out += math.log(col.like(v, prior))
                except ValueError:
                    return 0.0

        return math.exp(out)

    def d2h(self, data):
        d, n = 0, 0
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** 2
        return math.sqrt(d) / math.sqrt(n)

    def neighbors(self, data, rows=None):
        if rows is None:
            rows = data.rows
        return sorted(rows, key=lambda row: self.dist(row, data))

    def dist(self, other, data):
        d, n, p = 0, 0, self.the.p
        for col in data.cols.x:
            n += 1
            d += col.dist(self.cells[col.at], other.cells[col.at]) ** p
        return (d / n) ** (1 / p)

    # def dist_squared(self, other, data):
    #     d, n, p = 0, 0, self.the.p
    #     for col in data.cols.x:
    #         n += 1
    #         d += col.dist(self.cells[col.at], other.cells[col.at]) ** p
    #     return d / n
