import csv
from typing import Any, Dict, Hashable, List

import pandas


def read_financial_operations_from_csv_files(file_path: str) -> List[Dict[str, Any]]:
    """

    :param file_path:
    :return:
    """
    operations = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            operations.append(dict(row))
    return operations


# if __name__ in "__main__":
#     csv_transactions = read_financial_operations_from_csv_files('data/transactions.csv')
#     for transaction in csv_transactions:
#         print(transaction)


def read_financial_operations_from_xlsx_files(file_path: str) -> list[dict[Hashable, Any]]:
    """

    :param file_path:
    :return:
    """
    dataframe = pandas.read_excel(file_path)
    operations = dataframe.to_dict(orient="records")
    return operations


# if __name__ in "__main__":
#     xlsx_transactions = read_financial_operations_from_xlsx_files('data/transactions_excel.xlsx')
#
#     for transaction in xlsx_transactions:
#         if transaction.setdefault('id') == 5446796.0:
#             print("Транзакция:")
#             print(transaction)
#             break
#     else:
#         print(f"Транзакция с id не найдена.")
