# Verification certificate

## Claim

- For k=4..23 the values in `data/terms.txt` are the class minima, with the convention a(5)=0 for an empty class.
- Each stored witness has the Hamiltonian-cycle count reported for its order.

## Evidence

| What | Program | Author / date | Coverage | Result |
|---|---|---|---|---|
| Producer | `programs/hc2.c` | lab agent vtora, 2026-08-31, as attributed by source ledger; comments removed | source census 8..46, extracted in `data/source-census.csv` | reported values, not independently checked in full |
| Replayed producer | `programs/census.py`, `programs/hc2.c` | OpenAI Codex, 2026-11-13 (wrapper); vtora (counter) | 8..40, even | source minima agree; see logs |
| Independent counter | `verification/count.py` | OpenAI Codex, 2026-11-13 | stored minimizers | see `verification/logs/minimizers.txt` and `minimizers-42-46.txt` |
| Independent graph-class check | `verification/class_check.py` | OpenAI Codex, 2026-11-13 | all stored witnesses | simple cubic, bipartite, 3-connected and spherical rotation systems |
| Independent counter over census | `verification/census.py`, `verification/count.py` | OpenAI Codex, 2026-11-13 | every generated graph at even orders 8..26 | minima and graph counts agree |

The independent Python DFS shares neither cycle-counting code nor pruning with the C producer. It shares the generated graph input and relies on the same plantri generator, whose completeness is not independently checked. Witnesses give upper bounds on minima, not their lower bounds. The separate class checker verifies the supplied rotations are spherical by Euler characteristic, bipartiteness, and connectivity after all deletions of one or two vertices. It does not establish uniqueness or completeness.

## Replayed for this repository

2026-11-13, Darwin arm64. plantri 5.5 was downloaded from the URL in `programs/fetch-plantri.sh`, checked with `shasum -a 256` against the hash in that script, and compiled with `cc -O3`. Commands were run from the repository root using `/tmp/barnette-c4/plantri` and `/tmp/barnette-c4/hc2` as the two executables:

```sh
for n in 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38; do python3 programs/census.py "$n" /tmp/barnette-c4/plantri /tmp/barnette-c4/hc2; done
python3 programs/census.py 40 /tmp/barnette-c4/plantri /tmp/barnette-c4/hc2
python3 verification/census.py /tmp/barnette-c4/plantri
python3 verification/count.py data/minimizers/*.txt
python3 programs/find_min.py 42 40 /tmp/barnette-c4/plantri 480
python3 programs/find_min.py 46 44 /tmp/barnette-c4/plantri 480
python3 verification/count.py data/minimizers/42.txt data/minimizers/46.txt
python3 verification/class_check.py data/minimizers/*.txt
```

Full output is in `verification/logs/`. The independent census printed `n=26 graphs=57 min=24`; at 10 it printed `graphs=0 min=empty`. See the logs for every other order and witness. The source log's minimum profile at n=38 differs from the replay's 4^17 6^2 16^1 18^1, while both give 36; profiles describe witnesses, not uniqueness.

## Not covered

The census and minimum at n=42,44,46 have not been independently checked over the class. Independent cycle counting of the stored graphs verifies only those graph counts. A witness for each of these orders is stored and independently checked; it supplies an upper bound but not a class minimum. The original larger census was parallel, whereas on this machine full replay becomes substantially longer; full censuses at 42, 44 and 46 were not started under the ten-minute limit; the partial searches for witnesses are logged separately. The completeness and isomorphism-free generation of plantri are assumptions, not independently certified. No formula or eventual pattern is claimed, and the prior-art search does not establish novelty. The class checker does not independently enumerate the class.

## Guide's independent check

pending

## Verdict

partial — independent full-census cycle counts only through n=26, conditional on plantri; later minima and complete graph generation remain unverified independently.
