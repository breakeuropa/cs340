# tests_heap.py
# Run with: python3 tests_heap.py
# Assumes your class is in Heap.py and named Heap

import random
from Heap import Heap


def is_valid_max_heap(h: Heap) -> bool:
    """Check max-heap property for 1-based heap using heap_size."""
    for i in range(1, h.heap_size + 1):
        l = h.find_left(i)
        r = h.find_right(i)
        if l <= h.heap_size and h.A[i] < h.A[l]:
            return False
        if r <= h.heap_size and h.A[i] < h.A[r]:
            return False
    return True


def assert_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type:
        return
    except Exception as e:
        raise AssertionError(f"Expected {exc_type.__name__}, but got {type(e).__name__}: {e}")
    raise AssertionError(f"Expected {exc_type.__name__} to be raised, but no exception was raised.")


def test_index_formulas():
    h = Heap([10, 20, 30, 40, 50])
    # 1-based formulas expected
    assert h.find_left(1) == 2
    assert h.find_right(1) == 3
    assert h.find_parent(2) == 1
    assert h.find_parent(3) == 1
    assert h.find_left(3) == 6
    assert h.find_right(3) == 7
    print("✅ test_index_formulas passed")


def test_constructor_and_dummy():
    h = Heap()
    assert h.A == [None]
    assert h.heap_size == 0

    h2 = Heap([4, 1, 9])
    assert h2.A[0] is None
    assert h2.heap_size == 3
    assert h2.get_value(1) == 4  # before build_heap, it's just stored
    print("✅ test_constructor_and_dummy passed")


def test_get_value_bounds():
    h = Heap([5, 2, 8])
    assert_raises(IndexError, h.get_value, 0)
    assert_raises(IndexError, h.get_value, 4)
    print("✅ test_get_value_bounds passed")


def test_build_heap_basic():
    arr = [4, 1, 9, 2, 7, 3]
    h = Heap(arr)
    h.build_heap()
    assert h.A[0] is None
    assert h.heap_size == len(arr)
    assert is_valid_max_heap(h)
    assert h.A[1] == max(arr)
    print("✅ test_build_heap_basic passed")


def test_build_heap_with_parameter():
    h = Heap()
    h.build_heap([3, 1, 6, 5, 2, 4])
    assert h.heap_size == 6
    assert is_valid_max_heap(h)
    assert h.A[1] == 6
    print("✅ test_build_heap_with_parameter passed")


def test_heapify_single_call():
    # Force a case where heapify must fix node 1
    h = Heap([1, 10, 9, 8, 7, 6])
    # Make it 1-based, heap_size already set
    h.heap(1)
    assert is_valid_max_heap(h)
    assert h.A[1] == 10
    print("✅ test_heapify_single_call passed")


def test_extract_max_edge_cases():
    h = Heap()
    assert_raises(IndexError, h.extract_max)

    h2 = Heap([42])
    h2.build_heap()
    assert h2.extract_max() == 42
    assert h2.heap_size == 0
    assert h2.A == [None]  # after pop last
    print("✅ test_extract_max_edge_cases passed")


def test_extract_max_sequence():
    arr = [4, 1, 9, 2, 7, 3]
    h = Heap(arr)
    h.build_heap()

    extracted = []
    while h.heap_size > 0:
        extracted.append(h.extract_max())
        assert is_valid_max_heap(h)

    assert extracted == sorted(arr, reverse=True)
    print("✅ test_extract_max_sequence passed")


def test_insert_basic_and_multiple():
    h = Heap([10, 8, 5])
    h.build_heap()
    assert is_valid_max_heap(h)

    h.insert(15)
    assert is_valid_max_heap(h)
    assert h.A[1] == 15

    h.insert(3)
    assert is_valid_max_heap(h)

    h.insert(20)
    assert is_valid_max_heap(h)
    assert h.A[1] == 20

    # Extract all to verify descending order
    out = []
    while h.heap_size > 0:
        out.append(h.extract_max())
    assert out == sorted([10, 8, 5, 15, 3, 20], reverse=True)
    print("✅ test_insert_basic_and_multiple passed")


def test_heap_sort_output_and_no_crash():
    h = Heap()
    arr = [4, 1, 9, 2, 7, 3]
    sorted_arr = h.heap_sort(arr)
    assert sorted_arr == sorted(arr)

    # Try already-sorted and reverse-sorted
    arr2 = [1, 2, 3, 4, 5]
    arr3 = [9, 8, 7, 6, 5]
    assert h.heap_sort(arr2) == sorted(arr2)
    assert h.heap_sort(arr3) == sorted(arr3)
    print("✅ test_heap_sort_output_and_no_crash passed")


def test_duplicates_and_negatives():
    arr = [5, -1, 5, 0, -1, 5, 2]
    h = Heap(arr)
    h.build_heap()
    assert is_valid_max_heap(h)

    extracted = []
    while h.heap_size > 0:
        extracted.append(h.extract_max())
    assert extracted == sorted(arr, reverse=True)

    h2 = Heap()
    for x in arr:
        h2.insert(x)
        assert is_valid_max_heap(h2)
    extracted2 = []
    while h2.heap_size > 0:
        extracted2.append(h2.extract_max())
    assert extracted2 == sorted(arr, reverse=True)
    print("✅ test_duplicates_and_negatives passed")


def test_random_stress(seed=123, trials=50, n_min=1, n_max=100):
    random.seed(seed)

    for _ in range(trials):
        n = random.randint(n_min, n_max)
        arr = [random.randint(-1000, 1000) for _ in range(n)]

        # Test build_heap + repeated extract
        h = Heap(arr)
        h.build_heap()
        assert is_valid_max_heap(h)

        extracted = []
        while h.heap_size > 0:
            extracted.append(h.extract_max())
            assert is_valid_max_heap(h)
        assert extracted == sorted(arr, reverse=True)

        # Test insert-only + repeated extract
        h2 = Heap()
        for x in arr:
            h2.insert(x)
            assert is_valid_max_heap(h2)

        extracted2 = []
        while h2.heap_size > 0:
            extracted2.append(h2.extract_max())
            assert is_valid_max_heap(h2)
        assert extracted2 == sorted(arr, reverse=True)

        # Test heapsort
        h3 = Heap()
        assert h3.heap_sort(arr) == sorted(arr)

    print("✅ test_random_stress passed")


if __name__ == "__main__":
    test_index_formulas()
    test_constructor_and_dummy()
    test_get_value_bounds()
    test_build_heap_basic()
    test_build_heap_with_parameter()
    test_heapify_single_call()
    test_extract_max_edge_cases()
    test_extract_max_sequence()
    test_insert_basic_and_multiple()
    test_heap_sort_output_and_no_crash()
    test_duplicates_and_negatives()
    test_random_stress()

    print("\n🎉 ALL TESTS PASSED")
