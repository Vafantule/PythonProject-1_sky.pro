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
