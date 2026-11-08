# Assignment 3: Understanding Algorithm Efficiency and Scalability

**Course:** Algorithms and Data Structures (MSCS 532)  
**Author:** Tabbatha Jackson

This repository compares randomized and deterministic Quicksort and implements a hash table using separate chaining.

## Files

- `quicksort_analysis.py` — two three-way Quicksort implementations, correctness checks, and performance benchmarks across four input distributions and four input sizes.
- `hash_table.py` — integer-key hash table with insert, search, delete, a randomized multiply-add hash function, and dynamic resizing.
- `analysis_report.md` — theoretical analysis, original observed timings, and interpretation.

## Requirements

Python 3.10 or newer; no third-party packages.

## Run

```bash
python3 quicksort_analysis.py
python3 hash_table.py
```

## Quicksort methods

Randomized Quicksort selects its pivot uniformly at random using `random.choice`. Deterministic Quicksort selects the first element. Both use three-way partitions (`smaller`, `equal`, `larger`) to handle repeated keys.

Each new benchmark run tests input sizes 50, 100, 200, and 400 across random, sorted, reverse-sorted, and repeated-key arrays. It prints median timings of ten trials; actual results depend on the machine.

## Main findings

In the *initial single-run measurements* performed on the student's Mac, deterministic first-pivot Quicksort slowed substantially on sorted and reverse-sorted input. For example, with 400 already-sorted values, randomized Quicksort took 0.000588 seconds and deterministic Quicksort took 0.004243 seconds. See the report for all 16 comparisons. Rerunning the current benchmark code produces new results and is not expected to reproduce the original timings exactly.

Hashing with chaining allows multiple keys to share a bucket; expected lookup/insert/delete costs depend on the load factor. Resizing when the load factor exceeds 0.75 helps maintain short chains.

## Design notes

- Quicksort uses additional list allocations for readability and is not in-place.
- The deterministic first-pivot variant may reach Python's recursion limit on sufficiently large sorted input.
- The hash table supports integer keys and raises `KeyError` for missing keys. Insert updates existing keys without increasing its item count.
- Randomized hash coefficients are seeded for reproducibility in this educational example. A fixed seed is **not suitable for adversarial security**.

## Reference

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
