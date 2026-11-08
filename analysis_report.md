# Assignment 3: Understanding Algorithm Efficiency and Scalability

**Tabbatha Jackson**  
**Algorithms and Data Structures — MSCS 532**  
**November 2026**

## Part 1: Randomized Quicksort

### Implementation and edge cases

The file `quicksort_analysis.py` implements two versions of Quicksort. Randomized Quicksort chooses a pivot uniformly at random from its current subarray, while deterministic Quicksort always uses the first element. Both split values into less-than, equal-to, and greater-than partitions, recursively sort the outer partitions, and concatenate the results. The equal partition is important: repeated elements do not create repeated recursive calls. Empty and one-element arrays return immediately. The tradeoff is that this readable implementation allocates new lists rather than sorting in place.

### Expected-case analysis

For distinct keys with sorted ranks `i` and `j`, count one pivot–element encounter when the two keys first meet in a partition. The pair meets exactly when one of the two endpoints is the first pivot selected from ranks `i` through `j`, which has probability `2/(j-i+1)`. For each gap `d = j-i`, there are `n-d` pairs. By linearity of expectation, the expected number of encounters is `Σ (n-d) × 2/(d+1)`, summed from `d = 1` to `n-1`. This is at most `2n × Σ 1/(d+1) = O(n log n)` by the harmonic sum. Each partition does linear work in its subarray length, with a constant amount of work per encounter, so the expected running time is `O(n log n)`.

The random pivot prevents a fixed sorted input from consistently forcing extreme pivot choices; it does not eliminate the theoretical `O(n^2)` worst case. Three-way partitioning also improves behavior when there are many equal keys.

The first-pivot deterministic approach is particularly vulnerable to sorted and reverse-sorted data. On those inputs, one recursive partition is almost the entire remaining list; the recurrence becomes `T(n) = T(n-1) + O(n)`, resulting in `O(n^2)` time. Both variants use `O(n)` additional list storage per partition in this implementation, with recursion overhead dependent on partition shape.

### Empirical methodology

I used Python's `time.perf_counter()` to measure wall-clock running times on my Mac. Both algorithms received the same input per comparison, and each output was checked against Python's `sorted()`. The first set comprised *single trial* timings with array sizes 50, 100, 200, and 400. Distributions were random unique numbers, ascending, descending, and values repeated from 1 through 10. Measurements are shown in seconds and are subject to operating-system scheduling, interpreter overhead, and randomized pivot variability.

### Observed data — original single-run experiment

| n | Distribution | Randomized (s) | Deterministic (s) |
|---:|---|---:|---:|
| 50 | Random | 0.000042 | 0.000034 |
| 50 | Already sorted | 0.000034 | 0.000077 |
| 50 | Reverse sorted | 0.000031 | 0.000078 |
| 50 | Repeated elements | 0.000025 | 0.000015 |
| 100 | Random | 0.000083 | 0.000067 |
| 100 | Already sorted | 0.000072 | 0.000275 |
| 100 | Reverse sorted | 0.000073 | 0.000277 |
| 100 | Repeated elements | 0.000026 | 0.000028 |
| 200 | Random | 0.000175 | 0.000147 |
| 200 | Already sorted | 0.000159 | 0.001221 |
| 200 | Reverse sorted | 0.000151 | 0.001032 |
| 200 | Repeated elements | 0.000045 | 0.000049 |
| 400 | Random | 0.000376 | 0.000314 |
| 400 | Already sorted | 0.000588 | 0.004243 |
| 400 | Reverse sorted | 0.000394 | 0.003902 |
| 400 | Repeated elements | 0.000095 | 0.000092 |

### Interpretation

The sorted and reverse-sorted inputs show the clearest difference: at size 400, the randomized algorithm used 0.000588 seconds on sorted input compared with 0.004243 seconds for the first-pivot deterministic algorithm, about 7.2 times faster. For reverse-sorted input at the same size, the randomized version was about 9.9 times faster. This agrees with the analysis of balanced expected partitions versus consistently unbalanced partitions. On randomly ordered arrays, deterministic Quicksort was slightly faster in these short tests, possibly because choosing the first element avoids the overhead of a random choice. On repeated-element arrays, both were fast due to three-way partitioning.

These observations do not prove asymptotic complexity on their own: the arrays are modest, time measurements are tiny, and each row originally came from a single trial. The code now also provides repeatable-size experiments with ten timing repetitions and reports the median, a more reliable descriptive statistic for future runs. Median results are not fabricated or substituted for the observed data above.

## Part 2: Hashing with Chaining

### Implementation

The file `hash_table.py` defines a hash table with a list of buckets. Each bucket stores a chain of key-value pairs. A collision means two different integer keys map to the same bucket; chaining stores both without overwriting either. The `insert` operation updates an existing key or appends a new pair. The `search` operation scans the relevant bucket to return its value, and `delete` removes the matching pair. Missing keys raise `KeyError`.

To distribute integer keys, the implementation picks two coefficients `a` and `b` from a prime-modulus multiply-add hash family and maps the result into the current bucket range. Choosing coefficients from a universal-style hash family helps limit systematic collision patterns under the stated assumptions; the final reduction to an arbitrary bucket count means the implementation is best described as a practical approximation rather than a formal proof of universal hashing for every table size. The random seed makes demonstrations repeatable, not secure against an attacker.

### Expected time and load factor

Let `n` be the number of entries, `m` the number of buckets, and `α = n/m` the load factor. Under simple uniform hashing, the expected chain length is approximately `α`. Finding a key generally takes `O(1 + α)` expected time, while deletion needs a search and has the same expected bound. Insertion without duplicate checking can be constant-time by appending to the chain, but this implementation checks for an existing key first, giving `O(1 + α)` expected time. In a worst-case collision scenario all keys can land in one bucket, so these operations can degrade to `O(n)`.

The code grows the bucket count from `m` to `2m + 1` whenever the load factor exceeds 0.75. It rehashes the existing entries by calling `insert` for each one. Under simple uniform hashing, the expected cost of a resize is `O(n)`. Geometric growth spreads that cost over many insertions, giving expected amortized `O(1)` insertion time. If all entries collide, the repeated chain scans can make a single resize take `O(n²)`. A lower load factor uses more memory but reduces time spent scanning collisions. More advanced implementations can use proven universal families, prime-sized tables, and policies for shrinking tables after large deletions (Cormen et al., 2022).

### Implementation checks and limitations

The included smoke test inserts, updates, searches for, and deletes integer keys; it also inserts enough keys to trigger resizing and checks retrieval afterward. The design deliberately restricts keys to integers to make the hash function explicit and understandable. It is not a cryptographic hash table and should not use a publicly predictable random seed as a defense against deliberately selected adversarial keys.

## Conclusion

These exercises illustrate why performance depends not only on the algorithm name but on design choices and input structure. Random pivot selection usually protects Quicksort's expected running time from ordered-input effects. Three-way partitioning helps both methods handle duplicates. For hashing, keeping the load factor bounded helps chaining provide expected near-constant-time operations, at a cost in extra bucket memory and occasional rehashing.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
