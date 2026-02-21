# Heap.py
# Max-Heap implementation using 1-based indexing (dummy element at index 0)
# Required methods: find_left, find_right, find_parent, get_value, heap, build_heap,
#                   heap_sort, extract_max, insert

from __future__ import annotations
from typing import List, Optional, Any


class Heap:
    def __init__(self, array: Optional[List[int]] = None) -> None:
        """
        Constructor.
        Uses 1-based indexing by storing a dummy at index 0.
        If array is provided, stores it and can be heap-built via build_heap().
        """
        self.A: List[Optional[int]] = [None]  # index 0 dummy
        self.heap_size: int = 0

        if array is not None:
            # store as 1-indexed
            self.A = [None] + list(array)
            self.heap_size = len(array)

    def __del__(self) -> None:
        """Destructor (not usually necessary in Python, but included per instructions)."""
        # Clear references
        self.A = [None]
        self.heap_size = 0

    # ----------------------------
    # Part 1 required helpers
    # ----------------------------
    def find_left(self, i: int) -> int:
        """Return index of left child of node i (1-based)."""
        return 2 * i

    def find_right(self, i: int) -> int:
        """Return index of right child of node i (1-based)."""
        return 2 * i + 1

    def find_parent(self, i: int) -> int:
        """Return index of parent of node i (1-based)."""
        return i // 2

    def get_value(self, i: int) -> int:
        """
        Return the value at node index i.
        Raises IndexError if i is not within the current heap_size.
        """
        if i < 1 or i > self.heap_size:
            raise IndexError("Index out of heap range")
        # self.A[i] is Optional[int] in type hints, but will be int in valid range.
        return int(self.A[i])  # type: ignore[arg-type]

    def heap(self, i: int) -> None:
        """
        Heapify (Max-Heapify) at index i.
        Matches CLRS Heapify(A, i): sift-down to restore max-heap property.
        Running time: O(log n) worst-case.
        """
        # Iterative version (avoids recursion depth issues)
        while True:
            l = self.find_left(i)
            r = self.find_right(i)
            largest = i

            if l <= self.heap_size and self.A[l] is not None and self.A[largest] is not None:
                if self.A[l] > self.A[largest]:
                    largest = l

            if r <= self.heap_size and self.A[r] is not None and self.A[largest] is not None:
                if self.A[r] > self.A[largest]:
                    largest = r

            if largest == i:
                break

            # swap A[i] and A[largest]
            self.A[i], self.A[largest] = self.A[largest], self.A[i]
            i = largest

    def build_heap(self, array: Optional[List[int]] = None) -> None:
        """
        Build a max-heap from an input array (or from current stored array if None).
        Matches CLRS Build-Max-Heap:
            heap_size = n
            for i = floor(n/2) down to 1:
                heapify(i)

        Running time: O(n)
        """
        if array is not None:
            self.A = [None] + list(array)
            self.heap_size = len(array)

        # If no array passed, assumes self.A already has values and heap_size is set.
        for i in range(self.heap_size // 2, 0, -1):
            self.heap(i)

    # ----------------------------
    # Part 2 required functions
    # ----------------------------
    def extract_max(self) -> int:
        """
        Remove and return the maximum value in the heap (root at A[1]).
        Matches CLRS Heap-Extract-Max(A).
        Running time: O(log n)
        """
        if self.heap_size < 1:
            raise IndexError("heap underflow")

        max_val = int(self.A[1])  # root

        # Move last element to root
        self.A[1] = self.A[self.heap_size]
        # Remove last slot (optional, keeps list consistent with heap_size)
        self.A.pop()
        self.heap_size -= 1

        # Restore heap property
        if self.heap_size >= 1:
            self.heap(1)

        return max_val

    def insert(self, key: int) -> None:
        """
        Insert a value into the heap.
        Matches CLRS Heap-Insert(A, key) bubble-up logic.
        Running time: O(log n)
        """
        self.heap_size += 1

        # Ensure the underlying list has a slot for the new leaf
        if self.heap_size == len(self.A):
            self.A.append(None)
        else:
            self.A[self.heap_size] = None

        i = self.heap_size

        # "Shift parent down" style (as in slide) then place key at final position
        while i > 1 and self.A[self.find_parent(i)] is not None and int(self.A[self.find_parent(i)]) < key:
            self.A[i] = self.A[self.find_parent(i)]
            i = self.find_parent(i)

        self.A[i] = key

    def heap_sort(self, array: Optional[List[int]] = None) -> List[int]:
        """
        Sort using the heap (Heapsort).
        Typical heapsort:
            build max-heap
            for i = n down to 2:
                swap A[1], A[i]
                heap_size--
                heapify(1)

        Returns a NEW sorted list in ascending order.
        Running time: O(n log n)
        """
        # Build heap from provided array, or use current heap content
        if array is not None:
            self.build_heap(array)
        else:
            # If current content is not a heap yet, call build_heap() explicitly
            self.build_heap()

        original_size = self.heap_size

        # Perform in-place heapsort in the internal array
        for i in range(self.heap_size, 1, -1):
            # swap max (root) with end
            self.A[1], self.A[i] = self.A[i], self.A[1]
            self.heap_size -= 1
            self.heap(1)

        # Now self.A[1:original_size+1] is ascending (for max-heap heapsort)
        sorted_list = [int(x) for x in self.A[1:original_size + 1] if x is not None]

        # Restore heap_size (optional, but nice for continued use)
        self.heap_size = original_size

        return sorted_list


# Optional quick self-test (won't run unless you execute Heap.py directly)
if __name__ == "__main__":
    h = Heap([4, 1, 9, 2, 7, 3])
    h.build_heap()
    print("Heap array (1-indexed):", h.A)
    print("Extract max:", h.extract_max())
    print("After extract:", h.A)
    h.insert(10)
    print("After insert 10:", h.A)
    print("Heapsort:", h.heap_sort([4, 1, 9, 2, 7, 3]))
