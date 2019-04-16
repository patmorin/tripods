import sys
import collections


def print_matrix(s):
    for i in range(len(s)):
        print("|", end='')
        for j in range(len(s[i])):
            if s[i][j]:
                print(s[i][j], end='')
            else:
                print(" ", end='')
        print("|")

def add_col(s, j):
    return [ r[:j] + [None] + r[j:] for r in s ]

def add_row(s, i):
    cols = len(s[0])
    return s[:i] + [[None]*cols] + s[i:]

def dmin(a):
    if a: return min(a)
    return 1000

def dmax(a):
    if a: return max(a)
    return 0

def is_valid(tr, s):
    x, y, t = tr
    occupied = [(z[0],z[1]) for z in s]
    if (x,y) in occupied:
        return False
    ul = [z[2] for z in s if z[0] < x and z[1] >= y]
    lr = [z[2] for z in s if z[0] > x and z[1] <= y]
    right = [z[2] for z in s if z[0] > x and z[1] == y]
    left = [z[2] for z in s if z[0] < x and z[1] == y]
    above = [z[2] for z in s if z[0] == x and z[1] > y]
    below = [z[2] for z in s if z[0] == x and z[1] < y]
    if t in ul or t in lr or t in right or t in above:
        return False
    if dmin(left) <= t or dmax(right) >= t \
            or dmin(below) <= t or dmax(above) >= t:
        return False
    return True


if __name__ == "__main__":
    r = 3
    if len(sys.argv) == 2:
        r = int(sys.argv[1])

    q = collections.deque()
    q.append([(100,100,1)])
    print(q)
    best = 0
    while True:
        s = q.popleft()
        xs = [t[0] for t in s]
        ys = [t[1] for t in s]
        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        score = len(s)
        size = (maxx-minx) + (maxy-miny) + 2
        ratio = 2*score/size
        if ratio > best:
            best = ratio
            print(score, size, ratio)
            print(s)
        for x in range(minx-1, maxx+2):
            for y in range(miny-1, maxy+2):
                for t in range(1, r+1):
                    if is_valid((x,y,t), s):
                        q.append(s + [(x,y,t)])
