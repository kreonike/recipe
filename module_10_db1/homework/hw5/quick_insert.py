from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    left, right = 0, len(array)

    while left < right:
        mid = (left + right) // 2
        if array[mid] < number:
            left = mid + 1
        else:
            right = mid

    return left


if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
    assert find_insert_position([], 10) == 0
    assert find_insert_position([1, 2, 3], 0) == 0
    assert find_insert_position([1, 2, 3], 4) == 3
    assert find_insert_position([1, 2, 2, 3], 2) in [1, 2, 3]
