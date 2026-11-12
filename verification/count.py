#!/usr/bin/env python3
"""Count undirected Hamiltonian cycles by unpruned path enumeration."""
import sys
from pathlib import Path

def count(line):
    order, text = line.decode('latin-1').strip().split(' ', 1)
    g = [[ord(c)-97 for c in row] for row in text.split(',')]
    n = int(order)
    assert len(g)==n and all(len(set(row))==3 for row in g)
    assert all(0 <= v < n and u in g[v] and u != v for u,row in enumerate(g) for v in row)
    def visit(u, used, first):
        if used.bit_count() == n:
            return int(0 in g[u] and first < u)
        return sum(visit(v, used | (1 << v), first if u else v)
                   for v in g[u] if not (used >> v) & 1)
    return n, visit(0, 1, -1)

if __name__ == '__main__':
    for name in sys.argv[1:]:
        n, h = count(Path(name).read_bytes().split(b'\n')[0])
        print(f'{name}: n={n} cycles={h}', flush=True)
