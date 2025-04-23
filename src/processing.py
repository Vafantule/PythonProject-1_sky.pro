def filter_by_state(state: str) -> str:
    pass











def sort_by_date(sort_types, ascending=True):
    """
    Осуществляет сортировку массива данных по заданной переменной. Функция.
    :param sort_types: Массив данных.
    :param ascending: Направление сортировки.
    :return: Возвращает отсортированный список по заданной переменной.
    """
    sort_date = sorted(sort_types, key=lambda sort_type: sort_type.get("date"), reverse=ascending)
    return sort_date
