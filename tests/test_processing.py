import pytest
from src.processing import filter_by_state, sort_by_date
from typing import Any, Dict


## Блок тестирования 'sort_by_date'
@pytest.fixture
def sort_by_date_fixture():
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


def test_sort_by_date(operations: list, expected) -> None:
    assert sort_by_date(operations) == expected


@pytest.fixture
def not_correct_date():
    """
    Фикстура неправильной даты.
    :return:
    """
    return [{"date": "3215-654-9"}]


def test_correct_date(not_correct_date):
    """
    Тестирование функции на неправильный формат даты.
    :param not_correct_date: Некорректная дата.
    :return:
    """
    with pytest.raises(ValueError):
        sort_by_date(not_correct_date)
