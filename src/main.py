"""
Написать функцию,
которая получает на вход два списка чисел и возвращает новый список,
содержащий только те числа, которые встречаются в обоих списках.
"""

from typing import List


def get_sort_numbers(list_1: List[int], list_2: List[int]) -> List[int]:
    result = list(filter(lambda elem: elem in list_1, list_2))
    return result


if __name__ == "__main__":
    print(get_sort_numbers([1, 2, 3, 4], [3, 4, 5, 6]))
