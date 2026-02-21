# Heap Data Structure Implementation

## Overview

This project implements a Max-Heap data structure using 1-based indexing (with a dummy element at index 0). 

The following heap operations were implemented:

- find_left
- find_right
- find_parent
- get_value
- heap (Heapify)
- build_heap
- extract_max
- insert
- heap_sort

The heap follows the standard CLRS textbook algorithms.

---

## Running Time Analysis

Let n be the number of elements in the heap.

---

### 1. find_left(i)

Returns index of left child: 2i.

- Best Case: O(1)
- Worst Case: O(1)

This operation performs a single arithmetic calculation.

---

### 2. find_right(i)

Returns index of right child: 2i + 1.

- Best Case: O(1)
- Worst Case: O(1)

This operation performs a single arithmetic calculation.

---

### 3. find_parent(i)

Returns index of parent: floor(i / 2).

- Best Case: O(1)
- Worst Case: O(1)

This operation performs a single arithmetic calculation.

---

### 4. get_value(i)

Returns the value at index i.

- Best Case: O(1)
- Worst Case: O(1)

Array access takes constant time.

---

### 5. heap(i)  (Heapify)

Restores the max-heap property starting at node i.

- Best Case: O(1)  
  (when the node is already larger than its children)

- Worst Case: O(log n)  
  (when the element moves from root to leaf)

Reason: The height of a heap is log n, so at most log n swaps occur.

---

### 6. build_heap()

Builds a max-heap from an unordered array.

- Best Case: O(n)
- Worst Case: O(n)

Although heapify is O(log n), build_heap runs in linear time because:
- Half of the nodes are leaves (no work needed),
- Work decreases as we move down the tree.

This is a known result from heap analysis.

---

### 7. extract_max()

Removes and returns the maximum element (root).

Steps:
1. Replace root with last element.
2. Decrease heap size.
3. Call heap(1).

- Best Case: O(1)  
  (if heapify performs no swaps)

- Worst Case: O(log n)

Because heapify may move the element from root to leaf.

---

### 8. insert(key)

Inserts a new value into the heap.

Steps:
1. Add new leaf at the end.
2. Bubble up toward root.

- Best Case: O(1)  
  (if inserted key is smaller than its parent)

- Worst Case: O(log n)

Because the new element may move up to the root.

---

### 9. heap_sort()

Sorts the array using the heap.

Steps:
1. Build max-heap (O(n))
2. Repeatedly extract maximum (n times)

Total time:

- Best Case: O(n log n)
- Worst Case: O(n log n)

Heapsort always runs in O(n log n), regardless of input order.

---

## Space Complexity

- The heap uses O(n) space to store elements.
- No additional significant auxiliary space is used.
- Heapsort is an in-place sorting algorithm.

---

## Conclusion

This implementation follows the standard Max-Heap algorithms from lecture (CLRS style) using 1-based indexing. 

All priority queue operations:
- Maximum retrieval
- Extract-Max
- Insert

run efficiently in logarithmic time.
