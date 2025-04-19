"""
Написать функцию,
которая получает на вход два списка чисел и возвращает новый список,
содержащий только те числа, которые встречаются в обоих списках.
"""

from typing import List

def get_sort_numbers(list_1: List[int], list_2: List[int]) -> List[int]:
    result = list(filter(lambda elem: elem in list_1, list_2))
    return result
    # return list(set(list_1) & set(list_2))

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


"""
Написать функцию, 
которая получает на вход два списка чисел и возвращает новый список, 
содержащий только те числа, которые есть только в одном из списков.
"""


def get_not_sort_numbers(list_1: List[int], list_2: List[int]) -> List[int]:
    # result = list(filter(lambda element: element not in list_2, list_1))
    # return result
    list_3 = list(set(list_1) - set(list_2)) + list(set(list_2) - set(list_1))
    return list_3

# if __name__ == "__main__":
#     print(get_not_sort_numbers([1, 2, 3, 4], [3, 4, 5, 6]))


"""
Исправьте код, содержащий ошибки PEP 8 и плохой нейминг. 
Добавьте docstring и аннотации типов. Flake8 и mypy 
не должны выдавать ошибок.
"""


def circle_area(radius: int) -> int:
    """
    Вычисление радиуса по формуле. Функция.
    :param radius:
    :return:
    """
    PI = 3.14
    circleArea = PI * radius ** 2
    return circleArea

def format_description(radius, area):
    return "Radius is " + str(radius) + "; area is " + str(round(area, 2))

def get_info(radius: float):
    area = circle_area(radius)
    description = format_description(radius, area)
    print(description)

radius_final = int(input("Enter circle radius (int): "))
get_info(radius_final)