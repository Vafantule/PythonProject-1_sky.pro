from typing import List, Dict

def filter_by_state(select_values: List[Dict], state: str="EXECUTED") -> List[Dict]:
    select_value = [value for value in select_values if value.get("state") == state]
    return select_value


def sort_by_date(sort_types: List[Dict], reverse: bool=True) -> List[Dict]:
    """
    Осуществляет сортировку данных по заданной переменной. Функция.
    :param sort_types: Данные.
    :param reverse: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    sort_date = sorted(sort_types, key=lambda sort_type: sort_type.get("date"), reverse=True)
    return sort_date
