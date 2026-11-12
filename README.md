# OEIS candidate (no A-number yet): minimum Hamiltonian cycles in Barnette graphs

<!-- oeis-status:begin -->
**OEIS status: not submitted.** (replaced by the registry tool)
<!-- oeis-status:end -->

## Definition

For integer k >= 4, let a(k) be the minimum number of undirected Hamiltonian cycles among simple 3-connected cubic bipartite planar graphs on 2k vertices; if the class is empty, set a(k)=0. Offset 4. A cycle and its reverse count once, and rotations do not create new cycles. In particular the class is empty at k=5 (10 vertices), so the zero is a convention, not a minimum.

## Terms / result

| k | a(k) | k | a(k) |
|---:|---:|---:|---:|
| 4 | 6 | 14 | 16 |
| 5 | 0 | 15 | 28 |
| 6 | 8 | 16 | 18 |
| 7 | 12 | 17 | 32 |
| 8 | 10 | 18 | 20 |
| 9 | 16 | 19 | 36 |
| 10 | 12 | 20 | 22 |
| 11 | 20 | 21 | 40 |
| 12 | 14 | 22 | 24 |
| 13 | 24 | 23 | 44 |

The source reports all values; see `data/terms.txt` for machine-readable terms.

## How it was obtained

The source census generated Eulerian triangulations with plantri `-bc3`, took their duals with `-d`, then used `hc2.c` to enumerate undirected Hamiltonian cycles. The source aggregates count and minimum by vertex order. This repository repeats the census and keeps one embedding of each encountered minimizer. The separately constructed 44-vertex witness is an even prism; its neighbors are given in cyclic embedding order. Bytes in the plantri adjacency format are Latin-1, not UTF-8.

## Verification

An independently written path enumerator checks the cycle counts of the stored witnesses, and a separate checker tests their graph class and spherical embeddings; an independent count on every generated graph was run through 26 vertices. The full-class conclusion is conditional on plantri's generation being complete; the independent counter does not independently generate graphs. Later source claims and missing witnesses are identified in [CERTIFICATE.md](CERTIFICATE.md).

## Prior art and credit

Gibbons reported the same minimum table before the lab census by fable and vtora; plantri is by Brinkmann and McKay. A007083 counts the graph class. See [PRIOR-ART.md](PRIOR-ART.md) for searches, publications and limits on priority.

## Reproduce

With Python 3 and a C compiler, from the repository root:

```sh
sh programs/fetch-plantri.sh
cc -O3 programs/hc2.c -o hc2
python3 programs/census.py 26 ./plantri ./hc2
python3 verification/census.py ./plantri
python3 verification/count.py data/minimizers/*.txt
python3 verification/class_check.py data/minimizers/*.txt
```

The first census prints `n=26 SUMMARY graphs=57 ... minh=24`; the independent census prints graph counts 1,0,1,1,2,2,8,8,32,57 and corresponding minima 6,empty,8,12,10,16,12,20,14,24. Witness counts appear in `verification/logs/minimizers.txt` and `verification/logs/minimizers-42-46.txt`; the class-check log is `verification/logs/class.txt`. Fetching requires a network; the 42–46 cycle check is the slowest and can take several minutes on the recorded machine. Census commands overwrite minimizer files. Downloaded build artifacts should be kept untracked.

## Provenance

Source: `projects/science/barnette`, commit `3a25ee0144cfb45a380cc74ec0b6570bfbfa4256`, `code/hc2.c`, `data/hc2_n8-46.log`, `ledger.jsonl`. An English CSV extracts the graph totals, defect histogram and minima from the source census log; the original log remains at the source commit. The copied C program has its original non-English comments removed, with executable code unchanged. No source archive DOI was identified.

## Author, licence

Aleksei Kudriashov (ORCID 0009-0006-8885-5338), Athanor lab, with AI assistance (OpenAI Codex cores; Claude Code as the lab's guide). Code: MIT; data and text: CC BY 4.0 (see LICENSE.md).
