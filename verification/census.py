#!/usr/bin/env python3
import subprocess, sys
from count import count
for n in range(8, 28, 2):
    p = subprocess.run([sys.argv[1], '-adbc3', str(n//2+2)], capture_output=True, check=True)
    hs = [count(line)[1] for line in p.stdout.split(b'\n') if line]
    print(f'n={n} graphs={len(hs)} min={min(hs) if hs else "empty"}', flush=True)
