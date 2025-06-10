from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает новый список, отфильтрованный по указанному значению. Функция.
    :param transactions: Данные.
    :param state: Выбор значения, для отбора.
    :return: Возвращает список по заданной переменной.
    """
    # select_value = [value for value in transactions if value.get("state", "").upper() == state]
    select_value = [
        value for value in transactions
        if str(value.get("state", "")).strip().lower() == state.strip().lower()
    ]
    if not select_value:
        raise ValueError("Нет соответствующего значения.")
    return select_value


# if __name__ == "__main__":
#     print(filter_by_state([
#         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
# ))


# if __name__ == "__main__":
#     print(filter_by_state(transactions))


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Осуществляет сортировку данных по заданной переменной. Функция.
    :param transactions: Данные.
    :param reverse: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    try:
        sort_date = sorted(transactions, key=lambda sort_type: datetime.strptime(str(sort_type["date"])[:10],
                                                                                 "%Y-%m-%d"),
                                                                                 reverse=reverse)
        return sort_date
    except ValueError as error:
        print(f"Формат даты введен некорректно: ", error)
        raise


# if __name__ == "__main__":
#     print(sort_by_date(sort_types))
