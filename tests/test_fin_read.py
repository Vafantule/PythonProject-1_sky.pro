from typing import Any, Dict, List
from unittest.mock import mock_open, patch

import pandas
import pytest

from src.fin_read import read_financial_operations_from_csv_files, read_financial_operations_from_xlsx_files


# Блок тестирования чтения из cvs файла

@pytest.fixture
def csv_content() -> str:
    return ("id,state,date,amount,currency_name,currency_code,from,to,description\n"
            "2130098,PENDING,2020-06-07T11:11:36Z,30731,Euro,EUR,"
            "Visa 5749750597771353,American Express 9106381490184499,Перевод с карты на карту\n"
            "1867114,EXECUTED,2021-05-10T18:55:29Z,14544,Gourde,HTG,"
            "Mastercard 0767525826606493,Счет 76157683185767446509,Перевод организации\n"
            "5066038,CANCELED,2023-10-23T04:42:50Z,33373,Yuan Renminbi,CNY,"
            "Счет 76170734056444515565,Счет 16776970109008326532,Перевод со счета на счет")


@pytest.fixture
def csv_rows() -> List[Dict[str, Any]]:
    return [
        {
            "id": "2130098",
            "state": "PENDING",
            "date": "2020-06-07T11:11:36Z",
            "amount": "30731",
            "currency_name": "Euro",
            "currency_code": "EUR",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту"
        },
        {
            "id": "1867114",
            "state": "EXECUTED",
            "date": "2021-05-10T18:55:29Z",
            "amount": "14544",
            "currency_name": "Gourde",
            "currency_code": "HTG",
            "from": "Mastercard 0767525826606493",
            "to": "Счет 76157683185767446509",
            "description": "Перевод организации"},
        {
            "id": "5066038",
            "state": "CANCELED",
            "date": "2023-10-23T04:42:50Z",
            "amount": "33373",
            "currency_name": "Yuan Renminbi",
            "currency_code": "CNY",
            "from": "Счет 76170734056444515565",
            "to": "Счет 16776970109008326532",
            "description": "Перевод со счета на счет"
        },
    ]


def test_read_financial_operations_from_csv_files(csv_content: str, csv_rows: List[Dict[str, Any]]) -> None:
    with patch("builtins.open", mock_open(read_data=csv_content)):
        result = read_financial_operations_from_csv_files("fake.csv")
        assert result == csv_rows
        assert all(isinstance(row, dict) for row in result)
        assert set(result[0].keys()) == {
            "id", "state", "date", "amount",
            "currency_name", "currency_code",
            "from", "to", "description"
        }


@pytest.mark.parametrize("csv_data, expected", [
    ("id,state,date,amount,currency_name,currency_code,to,description\n"
     "3107343,EXECUTED,2023-01-25T13:33:00Z,33639,Krona,SEK,Счет 35662766798195077538,Открытие вклада\n",
     [{
         "id": "3107343",
         "state": "EXECUTED",
         "date": "2023-01-25T13:33:00Z",
         "amount": "33639",
         "currency_name": "Krona",
         "currency_code": "SEK",
         "to": "Счет 35662766798195077538",
         "description": "Открытие вклада"}]),
    (
        "id,state,date,amount,currency_name,currency_code,from,to,description\n",
        [],
    )
])
def test_read_financial_operations_from_csv_files_param(csv_data: str, expected: List[Dict[str, Any]]) -> None:
    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = read_financial_operations_from_csv_files("fake.csv")
        assert result == expected


def test_read_financial_operations_from_csv_files_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        read_financial_operations_from_csv_files("no_such_file.csv")


# Блок тестирования чтения из xlsx файла

@pytest.fixture
def xlsx_dataframe() -> pandas.DataFrame:
    data = {
        "id": ["1449073", "2029174"],
        "state": ["CANCELED", "EXECUTED"],
        "date": ["2021-05-11T10:06:51Z", "2022-08-09T17:12:27Z"],
        "amount": ["11834", "34143"],
        "currency_name": ["Rupiah", "Yuan Renminbi"],
        "currency_code": ["IDR", "CNY"],
        "from": ["Счет 17847122626293622323", "Visa 2717112074981212"],
        "to": ["Счет 68570011224094542755", "Discover 8397322380849617"],
        "description": ['Перевод со счета на счет', "Перевод с карты на карту"],
    }
    return pandas.DataFrame(data)


@pytest.fixture
def xlsx_rows() -> List[Dict[str, Any]]:
    return [
        {
            "id": "1449073",
            "state": "CANCELED",
            "date": "2021-05-11T10:06:51Z",
            "amount": "11834",
            "currency_name": "Rupiah",
            "currency_code": "IDR",
            "from": "Счет 17847122626293622323",
            "to": "Счет 68570011224094542755",
            "description": "Перевод со счета на счет",
        },
        {
            "id": "2029174",
            "state": "EXECUTED",
            "date": "2022-08-09T17:12:27Z",
            "amount": "34143",
            "currency_name": "Yuan Renminbi",
            "currency_code": "CNY",
            "from": "Visa 2717112074981212",
            "to": "Discover 8397322380849617",
            "description": "Перевод с карты на карту",
        },
    ]


def test_read_financial_operations_from_xlsx_files(
        xlsx_dataframe: pandas.DataFrame,
        xlsx_rows: List[Dict[str, Any]]
) -> None:
    with patch("pandas.read_excel", return_value=xlsx_dataframe) as mock_read_excel:
        result = read_financial_operations_from_xlsx_files("fake.xlsx")
        assert result == xlsx_rows
        mock_read_excel.assert_called_once_with("fake.xlsx")
        assert set(result[0].keys()) == {
            "id", "state", "date", "amount",
            "currency_name", "currency_code",
            "from", "to", "description"
        }


@pytest.mark.parametrize("dataframe_data, expected", [
    (
        {
            "id": [],
            "state": [],
            "date": [],
            "amount": [],
            "currency_name": [],
            "currency_code": [],
            "to": [],
            "description": [],
        },
        [],
    ),
    (
        {
            "id": [282352],
            "state": ["PENDING"],
            "date": ["2020-12-26T09:39:00Z"],
            "amount": [32566],
            "currency_name": ["Rupiah"],
            "currency_code": ["IDR"],
            "to": ["Счет 87117715624747483097"],
            "description": ["Открытие вклада"],
        },
        [
            {
                "id": 282352,
                "state": "PENDING",
                "date": "2020-12-26T09:39:00Z",
                "amount": 32566,
                "currency_name": "Rupiah",
                "currency_code": "IDR",
                "to": "Счет 87117715624747483097",
                "description": "Открытие вклада",
            }
        ],
    ),
])
def test_read_financial_operations_from_xlsx_file_param(
        dataframe_data: Dict[str, List],
        expected: List[Dict[str, Any]]
) -> None:
    dafaframe = pandas.DataFrame(dataframe_data)
    with patch("pandas.read_excel", return_value=dafaframe):
        result = read_financial_operations_from_xlsx_files("fake.xlsx")
        assert result == expected


def test_read_financial_operations_from_xlsx_files_not_found() -> None:
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_financial_operations_from_xlsx_files("no_such_file.xlsx")
