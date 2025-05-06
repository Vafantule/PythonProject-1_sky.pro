import pytest

from src.processing import filter_by_state, sort_by_date

# from typing import Any, Dict


@pytest.mark.parametrize("state, expected", [
    ("EXECUTED",
     [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]),
    ("CANCELED",
     [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]),
])
def test_filter_by_state(state: str, expected: str) -> None:
    """
    Тестирование функции сортировки по значению.
    :param state: Необходимое значение.
    :param expected: Ожидаемый результат.
    :return:
    """
    state_filter = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    assert filter_by_state(state_filter, state) == expected


# Блок тестирования 'filter_by_state'
# @pytest.fixture
# def state_filter():
#     return [
#         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
#     ]
#
#
# @pytest.mark.parametrize("state, expected", [
#     ("EXECUTED",
#      [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#      {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]),
#     ("CANCELED",
#      [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#      {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]),
#     ("pending", [])
# ])
#
#
# def test_filter_by_state(state: str, expected):
#     """
#     Тестирование функции сортировки по значению.
#     :param state: Необходимое значение.
#     :param expected: Ожидаемый результат.
#     :return:
#     """
#     state_filter = [
#         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
#     ]
#     assert filter_by_state(state_filter, state) == expected
#
#
# @pytest.fixture
# def sample_date() -> list[Dict[Any, Any]]:
#     return [
#         {"state": "EXECUTED", "value": 500},
#         {"state": "PENDING", "value": 150}
#     ]
#
#
# def test_filter_by_state_no_match(sample_date: list[Dict[Any, Any]]) -> None:
#     assert filter_by_state(sample_date, state="COMPLETED") == []
#
#
# @pytest.fixture
# def wrong_filter_by_state():
#     return ({"99"})
#
#
# def test_correct_filter_by_state() -> None:
#     with pytest.raises(ValueError):
#         filter_by_state(wrong_filter_by_state)
#

# Блок тестирования 'sort_by_date'
@pytest.fixture
def sort_by_date_fixture() -> list:
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]


@pytest.mark.parametrize("operations, expected", [
    ([{"date": "2009-07-03"}, {"date": "2019-07-03"}], [{"date": "2019-07-03"}, {"date": "2009-07-03"}]),
    ([{"date": "2029-12-31"}, {"date": "2019-01-01"}], [{"date": "2029-12-31"}, {"date": "2019-01-01"}]),
    ([{"date": "2019-02-28"}, {"date": "2019-02-28"}], [{"date": "2019-02-28"}, {"date": "2019-02-28"}])
])
def test_sort_by_date(operations: list, expected: list) -> None:
    assert sort_by_date(operations) == expected


@pytest.fixture
def not_correct_date() -> list:
    """
    Фикстура неправильной даты.
    :return:
    """
    return [{"date": "3215-654-9"}]


def test_correct_date(not_correct_date: list) -> None:
    """
    Тестирование функции на неправильный формат даты.
    :param not_correct_date: Некорректная дата.
    :return:
    """
    with pytest.raises(ValueError):
        sort_by_date(not_correct_date)
