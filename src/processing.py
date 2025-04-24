from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Отбор данных по заданному значению. Функция.
    :param transactions: Данные.
    :param state: Отбор значения.
    :return: Возвращает список по заданной переменной.
    """
    select_value = [value for value in transactions if value.get("state") == state]
    return select_value


def sort_by_date(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Осуществляет сортировку данных по заданной переменной. Функция.
    :param transactions: Данные.
    :param reverse: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    sort_date = sorted(transactions, key=lambda sort_type: sort_type["date"], reverse=True)
    return sort_date


# if __name__ == "__main__":
#     print(sort_by_date(sort_types))
