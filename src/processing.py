from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает новый список, отфильтрованный по указанному значению. Функция.
    :param transactions: Данные.
    :param state: Выбор значения, для отбора.
    :return: Возвращает список по заданной переменной.
    """
    select_value = [value for value in transactions if value.get("state") == state]
    return select_value


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Осуществляет сортировку данных по заданной переменной. Функция.
    :param transactions: Данные.
    :param reverse: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    sort_date = sorted(transactions, key=lambda sort_type: str(sort_type["date"]), reverse=reverse)
    return sort_date


# if __name__ == "__main__":
#     print(sort_by_date(sort_types))
