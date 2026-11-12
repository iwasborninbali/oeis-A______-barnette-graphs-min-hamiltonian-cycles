#!/usr/bin/env python3
"""Stream plantri graphs to the source counter, stopping at a target count.

Usage: python3 programs/find_min.py ORDER TARGET PLANTRI SECONDS
No exhaustiveness claim follows from finding a witness.
"""
import re, signal, subprocess, sys, tempfile, time
from pathlib import Path
n, target, plantri, limit = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
source = Path('programs/hc2.c').read_text()
source = source.replace('int main(int argc, char **argv){', 'int main(int argc, char **argv){ setvbuf(stdout, NULL, _IONBF, 0);', 1)
def deadline(signum, frame):
    raise TimeoutError('time limit reached')
signal.signal(signal.SIGALRM, deadline)
with tempfile.TemporaryDirectory() as tmp:
    cfile = Path(tmp)/'hc2.c'; exe = Path(tmp)/'hc2'
    cfile.write_text(source)
    subprocess.run(['cc', '-O3', str(cfile), '-o', str(exe)], check=True)
    gen = subprocess.Popen([plantri, '-adbc3', str(n//2+2)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    cnt = subprocess.Popen([str(exe), '-v'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    start = time.monotonic(); signal.alarm(limit)
    try:
        for i, graph in enumerate(gen.stdout, 1):
            cnt.stdin.write(graph); cnt.stdin.flush()
            result = cnt.stdout.readline()
            m = re.match(rb'G h=(\d+)', result)
            if not m: raise RuntimeError(repr(result))
            if int(m.group(1)) == target:
                Path(f'data/minimizers/{n}.txt').write_bytes(graph)
                print(f'n={n} target={target} found at graph={i} seconds={time.monotonic()-start:.1f}', flush=True)
                break
            if i % 10000 == 0:
                print(f'n={n} graphs_examined={i} seconds={time.monotonic()-start:.1f}', flush=True)
        else:
            print(f'n={n} target not found in complete stream', flush=True)
    except TimeoutError:
        print(f'n={n} time limit reached; no target found', flush=True)
    finally:
        signal.alarm(0)
        for proc in (gen, cnt):
            if proc.poll() is None: proc.kill()
            proc.wait()
