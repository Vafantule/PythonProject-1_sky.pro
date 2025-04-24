from typing import List, Dict

def filter_by_state(state: str="EXECUTED") -> str:
    pass











def sort_by_date(sort_types: List[dict], reverse:bool=True) -> List[dict]:
    """
    Осуществляет сортировку данных по заданной переменной. Функция.
    :param sort_types: Данные.
    :param reverse: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    sort_date = sorted(sort_types, key=lambda sort_type: sort_type.get("date"), reverse=reverse)
    return sort_date
