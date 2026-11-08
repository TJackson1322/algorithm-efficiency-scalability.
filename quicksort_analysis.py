"""Compare randomized and first-pivot deterministic quicksort.

Three-way partitioning handles repeated values efficiently.
Run: python3 quicksort_analysis.py
"""
import random
import statistics
import time

def randomized_quicksort(arr):
    if len(arr) <= 1:
        return arr.copy()
    pivot = random.choice(arr)
    smaller = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    larger = [x for x in arr if x > pivot]
    return randomized_quicksort(smaller) + equal + randomized_quicksort(larger)

def deterministic_quicksort(arr):
    if len(arr) <= 1:
        return arr.copy()
    pivot = arr[0]
    smaller = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    larger = [x for x in arr if x > pivot]
    return deterministic_quicksort(smaller) + equal + deterministic_quicksort(larger)

def measure_time(algorithm, arr):
    start = time.perf_counter()
    result = algorithm(arr)
    elapsed = time.perf_counter() - start
    assert result == sorted(arr), "Sorting result is incorrect"
    return elapsed

def make_cases(size, rng):
    return {
        "Random": rng.sample(range(size * 10), size),
        "Already Sorted": list(range(size)),
        "Reverse Sorted": list(range(size, 0, -1)),
        "Repeated Elements": [rng.randint(1, 10) for _ in range(size)],
    }

def run_benchmarks(sizes=(50, 100, 200, 400), repetitions=10, seed=532):
    rng = random.Random(seed)
    for size in sizes:
        print(f"\nInput Size: {size}")
        for name, data in make_cases(size, rng).items():
            # Same input for both algorithms; take median across repeated trials.
            randomized = [measure_time(randomized_quicksort, data) for _ in range(repetitions)]
            deterministic = [measure_time(deterministic_quicksort, data) for _ in range(repetitions)]
            print(f"{name}: Randomized = {statistics.median(randomized):.6f}s | "
                  f"Deterministic = {statistics.median(deterministic):.6f}s")

if __name__ == "__main__":
    numbers = [8, 3, 5, 1, 9, 2, 5, 7]
    print("Original list:", numbers)
    print("Sorted list:", randomized_quicksort(numbers))
    print("Deterministic sorted:", deterministic_quicksort(numbers))
    for sample in ([], [3], [4, 4, 4], list(range(20)), list(range(20, 0, -1))):
        assert randomized_quicksort(sample) == deterministic_quicksort(sample) == sorted(sample)
    print("\nSCALABILITY TEST RESULTS (median of 10 runs)")
    run_benchmarks()
