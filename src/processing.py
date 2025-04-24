from typing import Any, Dict, List


def filter_by_state(select_values: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Отбор данных по заданному значению. Функция.
    :param select_values: Данные.
    :param state: Отбор значения.
    :return: Возвращает список по заданной переменной.
    """
    select_value = [value for value in select_values if value.get("state") == state]
    return select_value


def sort_by_date(sort_types: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Осуществляет сортировку данных по заданной переменной. Функция.
    :param sort_types: Данные.
    :param reverse: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    sort_date = sorted(sort_types, key=lambda sort_type: sort_type["date"], reverse=True)
    return sort_date


# if __name__ == "__main__":
#     print(sort_by_date(sort_types))
