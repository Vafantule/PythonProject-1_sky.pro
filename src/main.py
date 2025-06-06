import re
from typing import List

"""
Написать функцию,
которая получает на вход два списка чисел и возвращает новый список,
содержащий только те числа, которые встречаются в обоих списках.
"""


def get_sort_numbers(list_1: List[int], list_2: List[int]) -> List[int]:
    result = list(filter(lambda elem: elem in list_1, list_2))
    return result
    # return list(set(list_1) & set(list_2))


# if __name__ == "__main__":
# print(get_sort_numbers([1, 2, 3, 4], [3, 4, 5, 6]))


"""
Написать функцию,
которая получает на вход список чисел и возвращает новый список,
содержащий только числа, которые являются палиндромами
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


def circle_area(radius: float) -> float:
    """
    Вычисление площади круга по формуле. Функция.
    :param radius:
    :return:
    """
    pi = 3.14
    circle_area = pi * radius**2
    return circle_area


def format_description(radius: float, area: float) -> str:
    """
    Отформатированный вывод площади круга.
    """
    return "Radius is " + str(radius) + "; area is " + str(round(area, 2))


def get_info(radius: float) -> None:
    """
    Вывод информации?
    :param radius:
    :return:
    """
    area = circle_area(radius)
    description = format_description(radius, area)
    print(description)

# if __name__ == "__main__":
    radius_final = int(input("Enter circle radius (int): "))
    get_info(radius_final)


# # Указываем путь к директории
# current_directory = os.listdir("../data")
# print(current_directory)

# Получаем список файлов
# files = os.listdir(current_directory)

# Выводим список файлов
# print(files)

# path = '/data/names.txt'
#
# directory_name = os.path.basename(path)
# print(directory_name)


# path = os.path.join(os.path.dirname(__file__), "data", "names.txt").replace('\\', '/')
# path = os.path.abspath("data/names.txt").replace('\\', '/')

def clear_names(file_name: str) -> list:
    """
    Очистка имен от ненужных символов. Функция
    :param file_name:
    :return:
    """
    formatted_names_list = list()
    with open('data/' + file_name, "r", encoding='utf-8') as names_file:
        names_list = names_file.read().split()
        for name_item in names_list:
            new_name = ''
            for symbol in name_item:
                if symbol.isalpha():
                    new_name += symbol
            if new_name.isalpha():
                formatted_names_list.append(new_name)
    return formatted_names_list


# def is_cyrillic(name_item: str) -> bool:
#     """
#     Проверка кириллицы. Функция
#     :param name_item:
#     :return:
#     """
#     return bool(re.search('[а-яА-Я]{2,}', name_item))


def is_cyrillic(name_item: str) -> bool:
    russian = [word for word in name_item if 1039 < ord(word[0])]
    return russian


def filter_russain_names(names_list: list) -> list:
    """
    Отбработка имен написанных на русском языке. Функция
    :param names_list:
    :return:
    """
    rus_names_list = list()
    for name_item in names_list:
        if is_cyrillic(name_item):
            rus_names_list.append(name_item)
    return rus_names_list


def filter_english_names(names_list: list) -> list:
    """
    Отбработка имен написанных на английском языке. Функция
    :param names_list:
    :return:
    """
    eng_names_list = list()
    for name_item in names_list:
        if not is_cyrillic(name_item):
            eng_names_list.append(name_item)
    return eng_names_list


def save_to_file(file_name: str, data: str) -> None:
    """
    Сохранение обработанных данных в файл.
    :param file_name:
    :param data:
    :return:
    """
    with open('data/' + file_name, "w", encoding='utf-8') as names_file:
        names_file.write(data)


# if __name__ == "__main__":
    cleared_names = clear_names('names.txt')
    print(is_cyrillic(cleared_names))
    # for index in cleared_names:
    filtered_names = filter_russain_names(cleared_names)
    save_to_file(
        "russsian_names.txt",
        "\n".join(filtered_names)
    )
    filtered_names = filter_english_names(cleared_names)
    save_to_file(
        "english_names.txt",
        "\n".join(filtered_names)
    )
