import math
import csv
import random
from sym import SYM
from rows import ROW
from cols import COLS
from util import Utility
from node import NODE


class Data:
    def __init__(self, the, src, fun=None):
        self.rows = []
        self.cols = None
        self.the = the
        self.util = Utility()
        self.adds(src, fun)

    def adds(self, src, fun=None):
        if isinstance(src, str):
            for s in self.util.csv(file=src):
                self.add(s, fun)
        else: 
            for x in (src or []):
                self.add(x, fun)
        return self
    
    def add(self, t, fun=None):
        if hasattr(t, 'cells'):
            row = t
        else:
            row = ROW(self.the, t)

        #print(self.cols)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        arr = []
        for col in cols or self.cols.all:
            arr.append(col.mid())
        return ROW(self.the, arr)

    def div(self, cols=None):
        arr = []
        for col in cols or self.cols.all:
            arr.append(col.div())
        return ROW(self.the, arr)

    def small(self):
        arr = []
        for col in self.cols.all:
            arr.append(col.small())
        return ROW(self.the, arr)

    def stats(self, cols=None, fun=None, ndivs=None):
        arr = {".N": len(self.rows)}
        columns_to_iterate = getattr(self.cols, cols or "y", [])
        #print (columns_to_iterate)

        for col in columns_to_iterate:
            value = getattr(type(col), fun or "mid")(col)
            arr[col.txt] = round(value, 2)
        return arr

    def clone(self, rows=None):
        new = Data(self.the)
        new.cols.names = self.cols.names
        for row in rows or []:
            new.add(row)
        return new

    def gate(self, budget0, budget, some):
        stats = []
        bests = []
        rows = self.util.shuffle(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        
        for i in range(1, budget+1):
            best, rest = self.bestRest(lite, len(lite)**some)
            todo, selected = self.split(best, rest, lite, dark)
            stats[i] = selected.mid()
            bests[i] = best.rows[0]
            lite.append(dark.pop(todo))
        
        return stats, bests

    def split(self, best, rest, lite_rows, dark_rows):
        selected = Data(self.the, self.cols.names)
        max_val = 1E30
        out = 1
        
        for i, row in enumerate(dark_rows):
            b = row.like(best, len(lite_rows), 2)
            r = row.like(rest, len(lite_rows), 2)
            if b > r:
                selected.add(row)
            tmp = abs(b + r) / abs(b - r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp
        
        return out, selected

    def bestRest(self, rows, wanted):
        rows.sort(key=lambda a: a.d2h(self))
        best = [self.cols['names']]
        rest = [self.cols['names']]
        
        for i, row in enumerate(rows):
            if i <= wanted:
                best.append(row)
            else:
                rest.append(row)
        
        return Data(self.the, best), Data(self.the, rest)
    
    def farapart(self, rows, sortp=None, a=None, b=None):
        far = int(len(rows) * self.the.Far) // 1
        evals = 1 if a else 2
        a = a or random.choice(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        return a, b, a.dist(b, self), evals
    
    def half(self,rows,sortp,before):
        some=self.util.many(rows,min(self.the.Half,len(rows)))
        a,b,C,d=self.farapart(some,sortp,before)
        def dist(row1,row2):
            return row1.dist(row2,self)
        def project(r):
            return (dist(r,a)**2+C**2 -dist(r,b)**2)/(2*C)
        as_, bs=[], []
        for n, row in enumerate(self.util.keysort(rows,project)):
            if n<=(len(rows)/2 -1):
                as_.append(row)
            else:
                bs.append(row)
        return as_,bs,C,dist(a,bs[0]), d

    def tree(self, sortp):
        evals = 0
        def _tree(data, above=None):
            nonlocal evals
            node = NODE(data)
            if len(data.rows)>2 * len(self.rows)** 0.5:
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows, sortp, above)
                evals = evals + evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node
        return _tree(self),evals
    
    def branch(self,stop=None  ):
        evals=1
        rest=[]
        if not stop:
            stop=(2*len(self.rows)**0.5)
        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals
            if len(data.rows) > stop:
                
                lefts, rights, left, _, _, _, _ = self.half(data.rows, True, above)
                evals += 1
                rest.extend(rights)
                return _branch(data.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals
        return _branch(self)