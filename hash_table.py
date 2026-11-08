"""Hash table with separate chaining, universal-family hashing and resizing.

Run: python3 hash_table.py
"""
import random

class HashTable:
    def __init__(self, capacity=11, max_load=0.75, seed=532):
        if capacity < 2 or not 0 < max_load < 1:
            raise ValueError("capacity must be >= 2 and 0 < max_load < 1")
        self._prime = 2_147_483_647
        rng = random.Random(seed)
        self._a = rng.randrange(1, self._prime)
        self._b = rng.randrange(self._prime)
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        self.max_load = max_load

    def _index(self, key):
        if not isinstance(key, int):
            raise TypeError("This implementation supports integer keys")
        return ((self._a * (key % self._prime) + self._b) % self._prime) % self._capacity

    def insert(self, key, value):
        bucket = self._buckets[self._index(key)]
        for index, (existing, _) in enumerate(bucket):
            if existing == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self.load_factor > self.max_load:
            self._resize(self._capacity * 2 + 1)

    def search(self, key):
        for existing, value in self._buckets[self._index(key)]:
            if existing == key:
                return value
        raise KeyError(key)

    def delete(self, key):
        bucket = self._buckets[self._index(key)]
        for index, (existing, value) in enumerate(bucket):
            if existing == key:
                del bucket[index]
                self._size -= 1
                return value
        raise KeyError(key)

    def _resize(self, new_capacity):
        old_items = [item for bucket in self._buckets for item in bucket]
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for key, value in old_items:
            self.insert(key, value)

    @property
    def load_factor(self):
        return self._size / self._capacity

    def __len__(self):
        return self._size

if __name__ == "__main__":
    table = HashTable(capacity=3)
    for key, value in [(7, "Maddax"), (18, "Walter"), (29, "Chase"), (7, "Updated")]:
        table.insert(key, value)
    assert table.search(7) == "Updated"
    assert table.search(18) == "Walter"
    assert len(table) == 3
    assert table.delete(29) == "Chase"
    assert len(table) == 2
    try:
        table.search(29)
        raise AssertionError("Deleted key should be missing")
    except KeyError:
        pass
    for key in range(100):
        table.insert(key + 100, f"value-{key}")
    assert all(table.search(key + 100) == f"value-{key}" for key in range(100))
    print(f"Hash table tests passed. Items: {len(table)}, load factor: {table.load_factor:.3f}")
