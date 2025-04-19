"""
Написать функцию,
которая получает на вход два списка чисел и возвращает новый список,
содержащий только те числа, которые встречаются в обоих списках.
"""

from typing import List

def get_sort_numbers(list_1: List[int], list_2: List[int]) -> List[int]:
    result = list(filter(lambda elem: elem in list_1, list_2))
    return result


# if __name__ == "__main__":
    # print(get_sort_numbers([1, 2, 3, 4], [3, 4, 5, 6]))


"""
Написать функцию, 
которая получает на вход список чисел и возвращает новый список, 
содержащий только числа, которые являются палиндромами.
"""

def palindrome_list(unformatted_string: List[int]) -> List[int]:
    # strint_lower = strint.lower()
    # return strint_lower == strint_lower[::-1]
    new_list = []
    for index in unformatted_string:
        if str(index) == str(index)[::-1]:
            new_list.append(index)
    return new_list


# if __name__ == "__main__":
    # print(palindrome_list([121, 123, 131, 34543]))
