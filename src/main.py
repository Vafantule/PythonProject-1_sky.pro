import sys
from datetime import datetime
from typing import Any, Dict, Hashable, List

from src.fin_read import read_financial_operations_from_csv_files, read_financial_operations_from_xlsx_files
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import mask_account_card

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


def filter_russian_names(names_list: list) -> list:
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
#     cleared_names = clear_names('names.txt')
#     print(is_cyrillic(cleared_names))
#     # for index in cleared_names:
#     filtered_names = filter_russain_names(cleared_names)
#     save_to_file(
#         "russsian_names.txt",
#         "\n".join(filtered_names)
#     )
#     filtered_names = filter_english_names(cleared_names)
#     save_to_file(
#         "english_names.txt",
#         "\n".join(filtered_names)
#     )


# Домашнее задание по уроку 13.2.

def print_transaction(transaction: Dict[str, Any]) -> None:
    """
    Форматированный вывод одной транзакции. Функция.
    :param transaction: Словарь с данными одной транзакции.
    """
    date_string = transaction.get("date", "")
    try:
        date = datetime.strptime(str(date_string)[:10], "%Y-%m-%d")
        date_string = date.strftime("%d.%m.%Y")
    except Exception:
        date_string = date_string[:10]

    description = transaction.get("description", "")

    # Сумма и валюта
    if "operationamount" in transaction:
        amount = transaction["operationamount"].get("amount", "")
        currency_info = transaction["operationamount"].get("currency", {})
        if isinstance(currency_info, dict):
            currency = currency_info.get("name", "") or currency_info.get("code", "")
        else:
            currency = ""
    else:
        amount = transaction.get("amount", "")
        currency = (transaction.get("currency_name")
                    or transaction.get("currency", "")
                    or transaction.get("currency_code", ""))
    from_string = transaction.get("from", "")
    to_string = transaction.get("to", "")
    from_masked = mask_account_card(str(from_string)) if from_string else ""
    to_masked = mask_account_card(str(to_string)) if to_string else ""

    if from_masked == "Номер некорректный":
        from_masked = ""
    if to_masked == "Номер некорректный":
        to_masked = ""
    print(f"\n{date_string} {description}")

    if from_masked and to_masked:
        print(f"{from_masked} -> {to_masked}")
    elif from_masked:
        print(f"{from_masked}")
    elif to_masked:
        print(f"{to_masked}")
    print(f"Сумма: {amount} {currency}")


def lower_keys(object_for_correction: Any) -> Any:
    """
    Рекурсивно приводит все ключи словарей к нижнему регистру. Функция.
    :param object_for_correction: Вводимое значение от пользователя.
    :return: Объект с приведёнными к нижнему регистру ключами.
    """
    if isinstance(object_for_correction, dict):
        return {str(key).lower(): lower_keys(value) for key, value in object_for_correction.items()}
    elif isinstance(object_for_correction, list):
        return [lower_keys(element) for element in object_for_correction]
    return object_for_correction


def main() -> None:
    """
    Основная функция, реализует консольный интерфейс для работы с банковскими транзакциями.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    transactions: List[Dict[str, Any]] = []

    while True:
        menu_choice = input("\nВаш выбор 1/2/3: ").strip()
        if menu_choice in {"1", "2", "3"}:
            break
        print("\nВыбирайте из 1, 2 или 3.")

    if menu_choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        transactions = load_transactions("data/operations.json")
    elif menu_choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        transactions = read_financial_operations_from_csv_files("data/transactions.csv")
    elif menu_choice == "3":
        print("\nДля обработки выбран XLSX-файл (Excel).")
        raw_transactions: list[dict[Hashable, Any]] = (
            read_financial_operations_from_xlsx_files("data/transactions_excel.xlsx"))
        transactions = [
            {str(key): value for key, value in transaction.items()}
            for transaction in raw_transactions]

    if not transactions:
        print("Не удалось загрузить транзакции из файла.")
        sys.exit(1)

    transactions = lower_keys(transactions)

    # Фильтрация по статусу
    available_state = {"executed", "canceled", "pending"}
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        )
        state = input("Ваш ввод: ").strip().upper()
        if state.lower() in available_state:
            break
        print(f"Статус операции {state} недоступен.")

    try:
        filtered_transactions = filter_by_state(transactions, state)
        print(f"Операции отфильтрованы по '{state}'")
    except ValueError as error:
        print(f"Не найдено ни одной транзакции со статусом: {state}. Завершение. {error}")
        sys.exit(0)

    # Сортировка по дате
    while True:
        sort_answer = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
        if sort_answer in {"да", "нет"}:
            break
        print("Необходимо выбрать 'да' или 'нет'.")
    if sort_answer == "да":
        while True:
            order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
            if order in {"по возрастанию", "по убыванию"}:
                break
            print("Необходимо выбрать 'по возрастанию' или 'по убыванию'.")
        reverse = order == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

    # Фильтрация по валюте
    while True:
        ruble_answer = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
        if ruble_answer in {"да", "нет"}:
            break
        print("Необходимо выбрать 'да' или 'нет'.")
    if ruble_answer == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    # Фильтрация по описанию в любом поле
    while True:
        description_answer = input("Отфильтровать список транзакций по "
                                   "определенному слову в описании? Да/Нет\n").strip().lower()
        if description_answer in {"да", "нет"}:
            break
        print("Необходимо выбрать 'да' или 'нет'.")
    if description_answer == "да":
        if not filtered_transactions and not transactions:
            print("Нет данных для фильтрации по слову.")
            return
        sample_transaction = filtered_transactions[0] if filtered_transactions else transactions[0]
        print("Доступные поля для фильтрации по слову:")
        for key in sample_transaction.keys():
            print(f" - {key}")
        field = input("Введите имя поля для поиска "
                      "(или оставьте пустым, чтобы искать по всем полям): ").strip().lower()
        word_string = input("Введите данные для поиска: ").strip().lower()
        if not field:
            filtered_transactions = [
                transaction for transaction in filtered_transactions
                if any(word_string in str(value).lower() for value in transaction.values())
            ]
        else:
            filtered_transactions = [
                transaction for transaction in filtered_transactions
                if word_string in str(transaction.get(field, "")).lower()
            ]

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}")
    for transaction in filtered_transactions:
        print_transaction(transaction)


if __name__ == "__main__":
    main()
