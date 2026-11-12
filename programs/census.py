#!/usr/bin/env python3
"""Generate an exhaustive census and retain one minimizer per order."""
import subprocess, sys, re
from pathlib import Path
n = int(sys.argv[1]); plantri, hc = sys.argv[2:4]
gen = subprocess.Popen([plantri, '-adbc3', str(n//2+2)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
raw, err = gen.communicate()
if gen.returncode: raise SystemExit(err.decode(errors='replace'))
p = subprocess.run([hc, '-v'], input=raw, stdout=subprocess.PIPE, check=True)
lines = p.stdout.split(b'\n'); graphs = raw.split(b'\n'); best = None; witness = None
for graph, result in zip(graphs, lines):
    if not graph: break
    match = re.match(rb'G h=(\d+)', result)
    if not match: raise RuntimeError(result)
    h = int(match.group(1))
    if best is None or h < best: best, witness = h, graph
summary = next(line for line in lines if line.startswith(b'SUMMARY '))
print(f'n={n}', summary.decode())
if witness is not None:
    Path('data/minimizers').mkdir(exist_ok=True)
    Path(f'data/minimizers/{n}.txt').write_bytes(witness+b'\n')
