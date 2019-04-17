import sys
import collections
import itertools

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

def bounding_box(s):
    xs = [t[0] for t in s]
    ys = [t[1] for t in s]
    return min(xs), max(xs), min(ys), max(ys)

def get_seeds(r):
    if r >= 5 and r <= 7:
        combos = itertools.combinations(range(r,0,-1), 3)
        return [ ((-2,0,c[0]), (-1,0,c[1]), (0,0,c[2])) for c in combos ]
    return [((0,0,1),)]

def print_matrix(s):
    minx, maxx, miny, maxy = bounding_box(s)
    for y in range(maxy, miny-1, -1):
        print("|", end='')
        for x in range(minx, maxx+1):
            e = [ t[2] for t in s if (t[0],t[1]) == (x,y) ]
            if e:
                print(e[0], end='')
            else:
                print(" ", end='')
        print("|")


if __name__ == "__main__":
    r = 3
    if len(sys.argv) == 2:
        r = int(sys.argv[1])

    q = collections.deque()
    qs = set()
    seeds = get_seeds(r)
    for s in seeds:
        qs.add(s)
        q.append(s)
    best = 0
    iteration = 0
    duplicates = 0
    while True:
        s = q.popleft()
        minx, maxx, miny, maxy = bounding_box(s)
        score = len(s)
        size = (maxx-minx) + (maxy-miny) + 2
        ratio = 2*score/size
        if ratio >= best:
            best = ratio
            print("\n{} {} {}".format(score, size, ratio))
            print_matrix(s)
        if iteration % 1000 == 0:
            print("\r{:10} {:10} {:10} {:10} {:5.4} {:3}".format(iteration, len(q), len(qs), duplicates, best, size), end='')
        iteration += 1
        for x in range(minx-1, maxx+2):
            for y in range(miny-1, maxy+2):
                for t in range(1, r+1):
                    if is_valid((x,y,t), s):
                        nt = tuple(sorted(s + ((x,y,t),)))
                        if not nt in qs:
                            q.append(nt)
                            qs.add(nt)
                        else:
                            duplicates += 1
