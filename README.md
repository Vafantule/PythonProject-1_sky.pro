``` shell
python
```

# Sky.pro_practice

Учебное задание по курсу Python школы Sky.pro

## Установка

### Для начала используйте клонирование репозитория на свое рабочее место:
```
git clone git@github.com:Vafantule/PythonProject-1_sky.pro.git
```

### Установить необходимые зависимости для корректной работы:
```
pip install -r requirements.txt
```




## Модуль processing

Модуль предоставляет функции для работы с банковскими операциями:

- `filter_by_state`: фильтрует операции по заданному состоянию.
- `sort_by_date`: сортирует операции по дате.

### Примеры использования:

```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 59402872, 'state': 'CANCELLED', 'date': '2018-09-17T21:27:25.241241'}
]

# Фильтрация операций с состоянием "EXECUTED"
executed_transactions = filter_by_state(transactions)

# Сортировка операций по дате в порядке убывания
sorted_transactions = sort_by_date(transactions)
```
## Модуль generators

Модуль предоставляет функции для работы с банковскими операциями:

- `filter_by_currency`: выдает транзакции по заданной валюте.
- `transaction_descriptions`: выводит описание каждой операции по очереди.
- `card_number_generator`: генерирует диапазон банковских карт.

### Примеры использования:

```aiignore


Функция `transaction_descriptions` находится в файле generators.py. Пример использования:

from transaction_descriptions import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": ""},
    {},
    {"description": 123},
    "not a dict"
]

for desc in transaction_descriptions(transactions):
    print(desc)

Вывод:

Перевод организации
Нет необходимого словаря.
Нет необходимого словаря.
Нет необходимого словаря.
```

### Запуск тестов для проверки стабильности кода:
```
Тестирование

Тесты находятся в файле test_generators.py и используют pytest.

Для запуска тестов:

Убедитесь, что оба файла (generators.py и test_generators.py) находятся в одной директории.

Выполните команду:

pytest test_transaction_descriptions.py -v
```

## Документация:

Для получения дополнительной информации обратитесь к [документации](README.md).

## Лицензия:

Этот проект не лицензирован.
